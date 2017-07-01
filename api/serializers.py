from django.contrib.auth.models import User
from rest_framework import serializers
from . import models
class UserSerializer(serializers.ModelSerializer):
	"""UserSerializer"""
	password = serializers.CharField(write_only=True, style={'input_type': 'password'})
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
		write_only_fields = ('password',)

class SupplierSerializer(serializers.ModelSerializer):
	"""Supplier Serializer"""
	class Meta:
		model = models.Supplier
		fields = ['id', 'name', 'longitude', 'latitude', 'price_index']
		read_only_fields = ['price_index']

class ItemTypeSerializer(serializers.ModelSerializer):
	"""ItemType Serializer"""
	class Meta:
		model = models.ItemType
		fields = ['id', 'name', 'typical_price']

class OnSaleItemSerializer(serializers.ModelSerializer):
	"""OnSaleItemSerializer"""
	class Meta:
		model = models.OnSaleItem
		fields = ['id','name', 'sale_price', 'num_items', 'discount', 'image_url',
		 'start_date', 'end_date', 'supplier', 'item_type']