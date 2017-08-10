from .models import Supplier,SupplierAlias,BarcodeItem,OnSaleItem,FullPriceItem,ItemType
import logging
import datetime
from decimal import *


logger = logging.getLogger(__name__)
#supplier is a Supplier model object, end_date is a datetime object
def addItemFromScanner(name,brand,full_price,size,barcode,on_sale,supplier,discount_type,end_date,location):
    try:
        barcodeitemlist = BarcodeItem.objects.filter(barcode=barcode)
        if barcodeitemlist.exists():
            barcodeitem = barcodeitemlist[0]
            if barcodeitem.name != name or barcodeitem.brand != brand or barcodeitem.full_price != full_price:
                #write into json
                return
        else:
            pass
            #create new barcode Item

        #FullPriceItem
        fullpriceitemlist = FullPriceItem.objects.filter(barcode_item=barcodeitem, supplier=supplier)
        if fullpriceitemlist.exists():
            fullpriceitem = fullpriceitemlist[0]
            if fullpriceitem.name != name or fullpriceitem.full_price != full_price:
                # write into json
                return
        else:
            createFullPriceItem(name=name, full_price=full_price, barcode_item=barcodeitem,
                                supplier=supplier, location=location)
            # create fullpriceitem

        #Check if it's Onsale
        if on_sale == True:
            fullpriceitem.on_sale = True
            fullpriceitem.save()
            onsaleitemlist = OnSaleItem.objects.filter(barcode_item=barcodeitem, supplier=supplier)
            if onsaleitemlist.exists():
                onsaleitem = onsaleitemlist[0]
                if onsaleitem.name != name or onsaleitem.full_price != full_price or onsaleitem.discount_type.lower() \
                        != discount_type.lower():
                    # write into json
                    return
            else:
                createOnSaleItem(name=name, full_price=full_price, discount_type=discount_type, end_date=end_date
                                 ,location=location, barcode_item=barcodeitem,supplier=supplier)
        return {'status':'success'}

    except Exception as ex:
        logger.error("AddItem error: " + ex.message, exc_info=True)
        return {'status':'failed'}

def createBarcodeItem(name,brand,size,barcode):
    item = BarcodeItem(name=name,brand=brand,size=size,barcode=barcode,num_items=1,itemtype=itemtype,
                       timestamp=datetime.datetime.today())


def createFullPriceItem(name,full_price,barcode_item,supplier,location):
    item = FullPriceItem(name=name,full_price=full_price,barcode_item=barcode_item,supplier=supplier,
                         location=location,timestamp=datetime.datetime.today())
    item.save()
    pass


def createOnSaleItem(name,full_price,discount_type,end_date,location,barcode_item,supplier):
    discount = Decimal(4.30)
    sale_price = Decimal(8.70)
    item = OnSaleItem(name=name,full_price=full_price,discount_type=discount_type,end_date=end_date,location=location,
                      barcode_item=barcode_item,supplier=supplier,timestamp=datetime.datetime.today(),discount=discount,
                      sale_price=sale_price)
    item.save()

def findItemType(name):
    pass