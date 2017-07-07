from .models import ItemType


def get_items_from_file(filename):
    f = open(filename, 'r', encoding="ISO-8859-1")
    lines = f.readlines()
    f.close()
    for line in lines:
        tokens = line.split(',')
        ItemType.objects.create(name=tokens[0], typical_price=0, health_index=0)
    
