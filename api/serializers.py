from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    """UserSerializer"""
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'password')
        write_only_fields = ('password',)


class SupplierSerializer(serializers.ModelSerializer):
    """Supplier Serializer"""
    class Meta:
        model = models.Supplier
        fields = ['id', 'name', 'company', 'price_index']


class ItemTypeSerializer(serializers.ModelSerializer):
    """ItemType Serializer"""
    class Meta:
        model = models.ItemType
        fields = ['id', 'name', 'typical_price', 'health_index']


class OnSaleItemSerializer(serializers.ModelSerializer):
    """OnSaleItemSerializer"""

    class Meta:

        model = models.OnSaleItem
        fields = ['id', 'name', 'sale_price', 'num_items', 'discount', 'image_url',
                  'start_date', 'end_date', 'supplier', 'item_type']


def on_sale_filter(shopping_list,supplier):
    class OnSaleItemFiltered(serializers.ListSerializer):
        def to_representation(self, data):
            data = data.filter(item_type__id__in=shopping_list)
            return super(OnSaleItemFiltered, self).to_representation(data)

    class OnSaleItemFilteredSerializer(serializers.ModelSerializer):
        """OnSaleItemSerializer"""
        class Meta:
            list_serializer_class = OnSaleItemFiltered
            model = models.OnSaleItem
            fields = ['id', 'name', 'sale_price', 'num_items', 'discount', 'image_url',
                      'start_date', 'end_date', 'supplier', 'item_type']

    class SupplierWithSalesSerializer(serializers.ModelSerializer):
        """Supplier Serializer with sales"""
        onsaleitem_set = OnSaleItemFilteredSerializer(many=True)

        class Meta:
            model = models.Supplier
            fields = ['id', 'name', 'company', 'price_index', 'onsaleitem_set']
            read_only_fields = ['price_index']

    return SupplierWithSalesSerializer
