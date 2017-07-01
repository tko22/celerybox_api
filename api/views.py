# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from . import serializers
from django.contrib.auth.models import User
from rest_framework import generics
from . import models

class UserList(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = serializers.UserSerializer

class SupplierList(generics.ListCreateAPIView):
	queryset = models.Supplier.objects.all()
	serializer_class = serializers.SupplierSerializer

class SupplierDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.Supplier.objects.all()
	serializer_class = serializers.SupplierSerializer

class ItemTypeList(generics.ListCreateAPIView):
	queryset = models.ItemType.objects.all()
	serializer_class = serializers.ItemTypeSerializer

class ItemTypeDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.ItemType.objects.all()
	serializer_class = serializers.ItemTypeSerializer

class OnSaleItemList(generics.ListCreateAPIView):
	queryset = models.OnSaleItem.objects.all()
	serializer_class = serializers.OnSaleItemSerializer

class OnSaleItemDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.OnSaleItem.objects.all()
	serializer_class = serializers.OnSaleItemSerializer