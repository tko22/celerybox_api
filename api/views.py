# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from . import serializers
from django.contrib.auth.models import User
from rest_framework import generics
from django.http import Http404
from .models import Supplier,ItemType,OnSaleItem
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer

class SupplierList(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer

class SupplierDetail(generics.RetrieveAPIView):
    queryset = Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer


#Use Google Maps API
@api_view(['GET'])
def stores_list(request,longitude,latitude):
    data = {'status':'success'}
    if request.method == 'GET':
        try:
            data = {'longitude': longitude}
        except Exception:
            data['status'] = 'failed'
        return Response(data)

@api_view(['GET'])
def supplier_sale_items(request,pk):
    data = {'status':'success'}
    if request.method == 'GET':
        try:
            store = Supplier.objects.get(pk=pk)
            items = store.onsaleitem_set.all()
            data = {'pk':pk, 'supplier_name':store.name,'price_index':store.price_index,'onsaleitems':items,
                        'status_code':status.HTTP_200_OK}
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