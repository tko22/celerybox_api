from django.conf.urls import url, include
from . import views
urlpatterns = [
    # url(r'^users/$', views.UserList.as_view()),
    # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

    url(r'^suppliers/$', views.SupplierList.as_view()),
    url(r'^suppliers/(?P<pk>[0-9]+)/$', views.SupplierDetail.as_view()),
    url(r'^suppliers/(?P<longitude>[+-]?([0-9]*[.])?[0-9]+)/(?P<latitude>[+-]?([0-9]*[.])?[0-9]+)/$', views.stores_list,
        name="store list"),
    url(r'^suppliers/(?P<pk>[0-9]+)/onsaleitems/$',
        views.supplier_sale_items, name="supplier on sale stuff"),

    url(r'^itemtypes/$', views.ItemTypeList.as_view()),
    url(r'^itemtypes/(?P<pk>[0-9]+)/$', views.ItemTypeDetail.as_view()),

    url(r'^onsaleitems/$', views.OnSaleItemList.as_view()),
    url(r'^onsaleitems/(?P<pk>[0-9]+)/$', views.OnSaleItemDetail.as_view()),
    url(r'^bestsuppliers/$', views.RetrieveStores.as_view()),
    url(r'^fullpriceitems/$', views.FullPriceItemList.as_view()),
    url(r'^fullpriceitems/(?P<pk>[0-9]+)/$', views.FullPriceItemDetailByBarcode,name="fully price item by barcode" ),
    url(r'items/$',views.addItem, name="addingItems"),
]
