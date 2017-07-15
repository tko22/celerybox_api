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

@api_view(['GET'])
def stores_list(request,longitude,latitude):
    if request.method == 'GET':
        data = {'long':longitude,'lat':latitude}
        return Response(data)
    def get_object(self, longitude,latitude):
        ret = {'status':'success'}
        try:
            ret['long'] = longitude
            ret['lat'] = latitude
            return HttpResponse(latitude)
        except Supplier.DoesNotExist:
            raise Http404

@api_view(['GET'])
def supplier_sale_items(request,pk):
    if request.method == 'GET':
        return Response({'pk':pk, 'stores':{'safeway','costco'}})

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