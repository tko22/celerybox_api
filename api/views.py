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
from api.getBestStore import getBestStore
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
        array of dictionaries ordered by distance
        'id': int (id of store in database)
        'distance': float (meters)
        name: string
        lng: Double (Longitude)
        lat: Double (Latitude
        place_id: string
            given to us by google maps place api
            client will need it to make api request to get more info on store
    list:
        a list of id's of the itemtypes in the user's shopping list
        all integers
    distance_pref:
        an integer from 0-9.0
        9.0: fully prefer cost over distance, 0.0: fully prefer distance over cost
    organic_pref:
        an integer from 0-9.0
        same as distance_pref with organic replacing distance

    example:
    {"list":[680,673,750,757,671],

    "stores":[
        {"distance":923.5870705724529,"name":"smart_&_final_extra!","lng":-121.841406,"lat":37.338822,"place_id":"ChIJneC7zjPNj4ARU-K-xPFtufk"},
        {"distance":1046.836180088878,"name":"story_supermarket","lng":-121.8525102,"lat":37.33285699999999,"place_id":"ChIJ4x_0DyvNj4ARLNysm6JLG2s"},
        {"distance":1151.277756640423,"name":"lion_supermarket","lng":-121.8540135,"lat":37.33140049999999,"place_id":"ChIJn5qrGmAtjoARA61ef5ELZPE"},
        {"distance":1209.888715820873,"name":"mi_pueblo_food_center","lng":-121.843099,"lat":37.341285,"place_id":"ChIJRTpWSzDNj4ARLhlyf19fzGM"},
        {"distance":1432.006075238638,"name":"lucky_7_supermarket","lng":-121.8277975,"lat":37.32314719999999,"place_id":"ChIJQckEy70yjoARZ5le2EbNsNM"},
        {"distance":1714.276549956156,"name":"walmart_supercenter","lng":-121.860402,"lat":37.3310208,"place_id":"ChIJPfEd8tTMj4ARuPTeEOO-2UU"},
        {"distance":1855.738711320839,"name":"lion_supermarket","lng":-121.8236898,"lat":37.3211811,"place_id":"ChIJ5TQVbr0yjoARK21Gfi0EXmE"},
        {"distance":1965.926968072466,"name":"foodmaxx","lng":-121.8205052,"lat":37.32386779999999,"place_id":"ChIJRZn44aIyjoARAtT99_jCzNg"},
        {"distance":2690.132394573325,"name":"safeway","lng":-121.8107428,"lat":37.3315158,"place_id":"ChIJv1SgbKcyjoARRLjiH5cRQ-c"},
        {"distance":2845.793281523308,"name":"fresco_supermarket","lng":-121.8100944,"lat":37.3237537,"place_id":"ChIJoXk04J8yjoARvmxNYsPbQl0"},
        {"distance":3130.600511127204,"name":"chaparral_supermarket","lng":-121.8705815,"lat":37.3460111,"place_id":"ChIJ38fRNOjMj4ARLmO7SOmHFfA"},
        {"distance":3487.64208603223,"name":"maxim_market","lng":-121.8112126,"lat":37.3100379,"place_id":"ChIJ9aaQlhy1j4ARuMYKiNiXgng"},
        {"distance":3571.580051494063,"name":"grocery_outlet_bargain_market","lng":-121.8583135,"lat":37.30141899999999,"place_id":"ChIJpSSFIx0zjoARJW1stv2JzVg"}
    ]

    "distance_pref":6.18864107131958,

    "organic_pref":5.823529243469238}

    NOTE: Posting a json text in the text box below does not work
    """

    def post(self,request,format=None):
        try:
            print 'post'
            try:
                data = request.body

                jsondata = json.loads(data)

            except Exception as ex:
                logger.error("views.RetrieveStores: loading request.body error" + ex.message,exc_info=True)
                return Response({'status':'failed','message':'Server Error: retrieving data'})
            ret = getBestStore(request,jsondata)
            return Response(ret)
            # #return JsonResponse(store_query,safe=False)

        except Exception as ex:
            ret = {}
            ret = {'status':'failed','status_code':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Something went Wrong! Wait and try again'}
            logger.error("views.RetrieveStores error: " + ex.message, exc_info=True)
            try:
                logger.error("views.RetrieveStores jsondata: " + jsondata)
            except:
                pass
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

class FullPriceItemList(generics.ListCreateAPIView):
    queryset = FullPriceItem.objects.all()
    serializer_class = serializers.FullPriceItemSerializer

@api_view(['GET'])
def FullPriceItemDetailByBarcode(request, barcode):
    data = {'status': 'success'}
    if request.method == 'GET':
        try:
            item = FullPriceItem.objects.get(barcode=barcode)
            serializer = serializers.FullPriceItemSerializer(item)
            return Response(serializer.data)
        except Exception:
            data['status'] = 'failed'
            data['status_code'] = status.HTTP_404
            data['message'] = "Couldn't get store with barcode:",barcode



# Add item to either OnSaleItem or FullPriceItem
# jsondata includes {
#   name(String),brand(String),price(String - will need to convert ex:4.00), size(String ex:4oz,6ct),
#   barcode(String),Location(String as lat,lng ex: 57.3874,128.17839 just copy and paste model),
#   supplier(it will be in format lowercase and underscore), on_sale(boolean) - if on sale -> try to find
#   if there is an item that inside the FullPriceItem with the same barcode and mark it on sale and add the item
#   to the OnSaleItem Table.
#  if its on sale, there will be another field name discount_type(String) -> if its dollar_amount there will be another
#  field name discount and that will the dollar amount discount else -> just copy the discount_type to discount_type



@api_view(['POST'])
def addItem(request):
    ret = {'status':'success'}
    if request.method =='POST':
        try:
            data = request.body
            jsondata = json.loads(data)



        except Exception as ex:
            logger.error("views.RetrieveStores: loading request.body error" + ex.message)
            return


