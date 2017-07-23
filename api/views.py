# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import serializers
from django.contrib.auth.models import User
from rest_framework import generics
from django.http import Http404
from .models import Supplier, ItemType, OnSaleItem
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.algorithm import retrieve_supplier


# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer

class RetriveStores(APIView):
    """
    An example of white the json data should look like.
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
                "id": 26,
                "distance": 8
            },
            {
                "id": 27,
                "distance": 5
            }
        ],
        "shopping_list": [
            122,
            8,
            3
        ],
        "preferences": {
            "distance": 4.5,
            "price": 8.4
        }
    }
    """

    def post(self, request, format=None):
        try:
            nearby_stores = {}
            for store in request.data['stores']:
                nearby_stores[store['id']] = store['distance']
            shopping_list = request.data['shopping_list']
            print(shopping_list)
            preferences = request.data['preferences']
            stores = retrieve_supplier(shopping_list, nearby_stores, preferences[
                                       'price'], preferences['distance'])
            store_query = []
            for store_index in range(0, len(stores)):
                store_query.append(Supplier.objects.get(id=stores[store_index]))
            serializer = serializers.on_sale_filter(
                shopping_list)(store_query, many=True)
            return Response(serializer.data)
        except Exception:
            data = {}
            data['status'] = 'failed'
            data['status_code'] = status.HTTP_404_NOT_FOUND
            return Response(data)


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
