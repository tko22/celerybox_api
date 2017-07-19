# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from api.models import *
from api.algorithm import *


class RetrieveSupplierTests(TestCase):

    def setUp(self):
        self.s1 = Supplier.objects.create(name='Store1', price_index=0.00)
        self.s2 = Supplier.objects.create(name='Store1', price_index=0.00)
        self.milk = ItemType.objects.create(name='Milk', category='Dairy',
                                            typical_price=0.00, health_index=0.00)
        OnSaleItem.objects.create(name='Special Milk', sale_price=3.00,
                                  discount=.25, num_items=1,
                                  supplier=self.s1, item_type=self.milk)

    def test_basic(self):
        shopping_list = [1]
        suppliers = {1: 4, 2: 4}
        price_preference = 5
        distance_preference = 5
        sorted_suppliers = retrieve_supplier(
            shopping_list, suppliers, price_preference, distance_preference)
        self.assertEqual(sorted_suppliers[0], 1)

    def test_price_index(self):
        self.milk.delete()
        self.s1.price_index = -1.00
        self.s1.save()
        shopping_list = [1]
        suppliers = {1: 4, 2: 4}
        price_preference = 5
        distance_preference = 5
        sorted_suppliers = retrieve_supplier(
            shopping_list, suppliers, price_preference, distance_preference)
        self.assertEqual(sorted_suppliers[0], 2)
