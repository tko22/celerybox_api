# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import serializers
from django.contrib.auth.models import User
from rest_framework import generics
from django.http import Http404
from .models import Supplier, ItemType, OnSaleItem, FullPriceItem, SupplierAlias
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from api.algorithm import retrieve_supplier
import logging
from django.http import QueryDict
from collections import OrderedDict
import traceback
# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
logger = logging.getLogger(__name__)
class RetrieveStores(APIView):
    """
    An example of what the json data should look like.
    stores:
        a list of dictionaries with keys id and distance
        'id': int (id of store in database)
        'distance': float (miles)
    shopping_list:
        a list of id's of the itemtypes in the user's shopping list
        all integers
    preferences:
        dictionary with keys distance and price
        'distance': float
        'price': float
        (Both between 0 to 9.99)
    {
        "stores": [
            {
                "id": 2,
                "distance": 8
            },
            {
                "id": 6,
                "distance": 5
            }
        ],
        "shopping_list": [
            182,
            8,
            3
        ],
        "preferences": {
            "distance": 4.5,
            "price": 8.4
        }
    }

    NOTE: Posting a json text in the text box below does not work
    """

    def post(self,request,format=None):
        ret = {'status': 'success'}
        try:
            print 'post'
            try:
                data = request.body
                jsondata = json.loads(data)
            except Exception as ex:
                logger.error("views.RetrieveStores: loading request.body error" + ex.message)
            stores_map = {}
            if len(jsondata['stores']) == 0:
                ret['status'] = 'failed'
                ret['message'] = 'Cannot find any stores. Your location may not be supported. Email us to add your location!'
                Response(ret)
            try:
                for store in jsondata['stores']:
                    filtered = Supplier.objects.filter(name__contains = store['name'])

                    if filtered.count() == 0:
                        second_filtered = SupplierAlias.objects.filter(alias__contains = store['name'])
                        if second_filtered.count() != 0:
                            if second_filtered[0].supplier.pk in stores_map:
                                continue
                            else:
                                stores_map[second_filtered[0].supplier.pk] = store
                    elif filtered.count() > 1:
                        logger.error("Filtered Multiple Stores",filtered,"name:",store['name'])
                    else:
                        if filtered[0].pk in stores_map:
                            continue
                        else:
                            stores_map[filtered[0].pk] = store
            except Exception as ex:
                logger.error("error mapping stores to stores in database" + ex.message)
                logger.error("data: " + jsondata)
                ret['status'] = 'failed'
                ret['message'] = 'Server Error'
                ret['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
                return Response(ret)

            if len(stores_map) == 0:
                ret['status'] = 'failed'
                ret['message'] = 'Cannot find any stores. Your location may not be supported. Email us to add your location!'
                Response(ret)
            nearby_stores = {}
            for key,info in stores_map.iteritems():
                nearby_stores[key] = info['distance']
            shopping_list = jsondata['list']
            preferences = {}
            distance_pref = jsondata['distance_pref']
            organic_pref = jsondata['organic_pref'] #NOT implemented in algorithm yet
            preferences['price'] = distance_pref / 2 #TEMP
            preferences['distance'] = distance_pref / 2 #TEMP
            stores = retrieve_supplier(shopping_list, nearby_stores, preferences[
                                       'price'], preferences['distance'])
            store_query = []
            if len(stores) == 0:
                ret['status'] = 'failed'
                ret['message'] = 'Cannot find any stores. Your location may not be supported. Email us to add your location!'
                return Response(ret)
            for store_index in range(0, len(stores)):
                onsaleitems = Supplier.objects.get(pk=stores[store_index]).onsaleitem_set.all()
                query_set = onsaleitems.filter(item_type__id__in=shopping_list)
                serializer = serializers.OnSaleItemSerializer(query_set, many=True)
                store = stores_map[stores[store_index]]

                store['onsaleitem_set'] = serializer.data

                store_query.append(store)


            ret['stores'] = store_query
            return Response(ret)
            #return JsonResponse(store_query,safe=False)
            # return Response({'status':'success'})
        except Exception as ex:
            ret['status'] = 'failed'
            ret['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            ret['message'] = 'Something went Wrong! Wait and try again'
            logger.error("views.RetrieveStores error: " + ex.message , traceback.print_exc())
            logger.error("views.RetrieveStores jsondata: " + jsondata)
            return Response(ret)


class SupplierList(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer


class SupplierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer


# Use Google Maps API
@api_view(['GET'])
def stores_list(request, longitude, latitude):
    data = {'status': 'success'}
    if request.method == 'GET':
        try:
            data = {'longitude': longitude}
        except Exception:
            data['status'] = 'failed'
        return Response(data)

@api_view(['GET'])
def supplier_sale_items(request, pk):
    data = {'status': 'success'}
    if request.method == 'GET':
        try:
            store = Supplier.objects.get(pk=pk)
            items = store.onsaleitem_set.all()
            data = {'pk': pk, 'supplier_name': store.name, 'price_index': store.price_index, 'onsaleitems': items,
                    'status_code': status.HTTP_200_OK}
        except Exception:
            data['status'] = 'failed'
            data['status_code'] = status.HTTP_404_NOT_FOUND
            return Response(data)
        return Response(data)


class ItemTypeList(generics.ListCreateAPIView):
    queryset = ItemType.objects.all()
    serializer_class = serializers.ItemTypeSerializer


class ItemTypeDetail(generics.RetrieveAPIView):
    queryset = ItemType.objects.all()
    serializer_class = serializers.ItemTypeSerializer


class OnSaleItemList(generics.ListCreateAPIView):
    queryset = OnSaleItem.objects.all()
    serializer_class = serializers.OnSaleItemSerializer


class OnSaleItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OnSaleItem.objects.all()
    serializer_class = serializers.OnSaleItemSerializer
