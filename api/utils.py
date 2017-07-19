from .models import ItemType, Supplier
from decimal import Decimal
from random import randint


def get_items_from_file(filename):
    f = open(filename, 'r', encoding="ISO-8859-1")
    lines = f.readlines()
    f.close()
    for line in lines:
        tokens = line.split(',')
        ItemType.objects.create(
            name=tokens[0], typical_price=0, health_index=0, category=tokens[1])


def random_decimal():
    ones = str(randint(0, 4))
    if randint(0, 1):
        ones = '-' + ones
    decimals = str(randint(0, 9)) + str(randint(0, 9))
    return Decimal(ones + '.' + decimals)


def get_suppliers_from_file(filename):
    f = open(filename, 'r', encoding="ISO-8859-1")
    lines = f.readlines()
    f.close()
    for line in lines:
        tokens = line.split(',')
        Supplier.objects.create(name=tokens[0], price_index=random_decimal())
