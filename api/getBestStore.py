from .models import Supplier, ItemType, OnSaleItem, FullPriceItem, SupplierAlias

import json
from api.algorithm import retrieve_supplier
import logging
import traceback
from . import serializers
from rest_framework import status

logger = logging.getLogger(__name__)
def getBestStore(request,jsondata):
    print "getBestStore"
    ret = {'status': 'success'}

    stores_map = {}
    if len(jsondata['stores']) == 0:
        ret = {'status': 'failed',
               'message': 'Cannot find any stores. Your location may not be supported. Email us to add your location!'}
        return ret
    try:
        for store in jsondata['stores']:
            filtered = Supplier.objects.filter(name__contains=store['name'])

            if filtered.count() == 0:
                second_filtered = SupplierAlias.objects.filter(alias__contains=store['name'])
                if second_filtered.count() != 0:
                    if second_filtered[0].supplier.pk in stores_map:
                        continue
                    else:
                        store["db_name"] = second_filtered[0].supplier.name
                        stores_map[second_filtered[0].supplier.pk] = store
            elif filtered.count() > 1:
                logger.error("Filtered Multiple Stores", filtered, "name:", store['name'])
            else:
                if filtered[0].pk in stores_map:
                    continue
                else:
                    store["db_name"] = filtered[0].name
                    stores_map[filtered[0].pk] = store
    except Exception as ex:
        logger.error("error mapping stores to stores in database" + ex.message, exc_info=True)
        logger.error("data: " + jsondata)
        ret = {'status':'failed','message':'Server Error','status_code':status.HTTP_500_INTERNAL_SERVER_ERROR}
        return ret

    if len(stores_map) == 0:
        ret = {'status': 'failed',
               'message': 'Cannot find any stores. Your location may not be supported. Email us to add your location!'}
        return ret
    nearby_stores = {}
    for key, info in stores_map.iteritems():
        nearby_stores[key] = info['distance']
    shopping_list = jsondata['list']
    preferences = {}
    distance_pref = jsondata['distance_pref']
    organic_pref = jsondata['organic_pref']  # NOT implemented in algorithm yet
    preferences['price'] = distance_pref / 2  # TEMP
    preferences['distance'] = distance_pref / 2  # TEMP
    try:
        stores = retrieve_supplier(shopping_list, nearby_stores, preferences[
            'price'], preferences['distance'])
    except Exception as ex:
        logger.error("Algorithm Error" + ex.message, exc_info=True)
        ret = {'status':'failed','message':"Server Error: Couldn't find the best store"}
        return ret
    try:
        store_query = []
        if len(stores) == 0:
            ret = {'status':'failed','message':'Cannot find any stores. Your location may not be supported. Email us to add your location!'}
            return ret
        for store_index in range(0, len(stores)):
            onsaleitems = Supplier.objects.get(pk=stores[store_index]).onsaleitem_set.all()
            query_set = onsaleitems.filter(item_type__id__in=shopping_list)
            serializer = serializers.OnSaleItemSerializer(query_set, many=True)
            store = stores_map[stores[store_index]]

            store['onsaleitem_set'] = serializer.data
            store_query.append(store)
        ret['stores'] = store_query
    except Exception as ex:
        logger.error("Serializers" + ex.message, exc_info=True)
        ret = {'status':'failed','message':"Server Error: Couldn't get OnSaleItems"}
        return ret
    return ret
    # return JsonResponse(store_query,safe=False)
    # return Response({'status':'success'})