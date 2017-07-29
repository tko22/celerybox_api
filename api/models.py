# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from decimal import Decimal


class Supplier(models.Model):
    name = models.CharField(max_length=50)
    #name this field keywords
    logo_url = models.CharField(max_length=100)
    company = models.CharField(max_length=20, default="None")
    # rank score, the higher the better, for price only
    price_index = models.DecimalField(
        max_digits=3, decimal_places=2, default=Decimal('0.00'))

    # latitude = models.DecimalField(max_digits=10, decimal_places=7)
    # longitude = models.DecimalField(max_digits=10, decimal_places=7)

    def __str__(self):
        return self.name + ' (Supplier #' + str(self.id) + ')'
class SupplierAlias(models.Model):
    alias = models.CharField(max_length=50)
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE) # names given in Google Maps API, without ' or -

    def __str__(self):
        return self.alias

class ItemType(models.Model):
    name = models.CharField(max_length=100,unique=True)
    typical_price = models.DecimalField(max_digits=6, decimal_places=2)
    health_index = models.FloatField(default=0)
    category = models.CharField(max_length=30)

    keywords = models.CharField(max_length=50,blank=True,null=True)
    def __str__(self):
        return self.name


class OnSaleItem(models.Model):
    name = models.CharField(max_length=250)
    brand = models.CharField(max_length=100)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)
    num_items = models.PositiveIntegerField()  # 1:0-5,2:5-10,3:over 10
    size = models.CharField(max_length=20)  # ex: 4ct,8oz
    full_price = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)  # in dollars
    discount = models.DecimalField(max_digits=4, decimal_places=2)
    discount_type = models.CharField(
        max_length=250)  # ex: Buy One get One free - if == dollar_amount -> look at full_price

    image_url = models.CharField(max_length=350)
    start_date = models.DateField()
    end_date = models.DateField()

    timestamp = models.DateField(auto_now=True)
    location = models.CharField(max_length=100, blank=True, null=True)  # lat,lng ex: 37.275937,128.58593

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + '(' + str(self.start_date) + ' - ' + str(self.end_date) + ')'


class FullPriceItem(models.Model):
    name = models.CharField(max_length=250)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    size = models.CharField(max_length=20)  # ex: 4ct,8oz
    num_items = models.PositiveIntegerField()  # 1:0-5,2:5-10,3:over 10
    image_url = models.CharField(max_length=350)

    barcode_num = models.CharField(max_length=14, blank=True, null=True)

    location = models.CharField(max_length=100)  # location it was added at - lat,lng ex: 37.275937,128.58593
    timestamp = models.DateField(auto_now=True)
    on_sale = models.BooleanField(default=False)  # an onsaleitem will be added 

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + '(' + self.supplier + ') as ' + self.item_type
