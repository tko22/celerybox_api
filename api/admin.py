# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Supplier,ItemType,OnSaleItem,FullPriceItem

# Register your models here.
admin.site.register(Supplier)
admin.site.register(ItemType)
admin.site.register(OnSaleItem)
admin.site.register(FullPriceItem)

