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

    keywords = models.CharField(max_length=50,blank=True)
    
    def __str__(self):
        return self.name

class BarcodeItem(models.Model):
    name = models.CharField(max_length=150,blank=True)
    brand = models.CharField(max_length=50,blank=True)
    size = models.CharField(max_length=20,blank=True) # ex: 4ct,8oz
    num_items = models.PositiveIntegerField() # 1:0-5,2:5-10,3:over 10
    image_url = models.CharField(max_length=350,blank=True)
    barcode = models.CharField(max_length=15,blank=True,unique=True)
    updated = models.DateField(blank=True)
    item_type = models.ForeignKey(ItemType, on_delete=models.SET_NULL,null=True)
    
    def __str__(self):
        return self.name + ":" + self.barcode
    

class OnSaleItem(models.Model):
    name = models.CharField(max_length=250, blank=True)
    
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)
    full_price = models.DecimalField(max_digits=4, decimal_places=2)  # in dollars
    
    discount = models.DecimalField(max_digits=4, decimal_places=2,blank=True)
    discount_type = models.CharField(
        max_length=250,blank=True)  # ex: Buy One get One free - if == dollar_amount -> look at full_price

    end_date = models.DateField()

    timestamp = models.DateField() # when it was updated
    location = models.CharField(max_length=100, blank=True)  # lat,lng ex: 37.275937,128.58593
    
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL,null=True)
    barcode_item = models.ForeignKey(BarcodeItem, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name + ": " + str(self.end_date) 


class FullPriceItem(models.Model):
    name = models.CharField(max_length=250,blank=True)
    full_price = models.DecimalField(max_digits=6, decimal_places=2)

    location = models.CharField(max_length=100,blank=True)  # location it was added at - lat,lng ex: 37.275937,128.58593
    
    timestamp = models.DateField()
    on_sale = models.BooleanField(default=False)  # an onsaleitem will be added 

    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL,null=True)
    barcode_item = models.ForeignKey(BarcodeItem, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name + '(' + self.supplier + ') as ' + self.barcode_item
