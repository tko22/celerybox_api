from django.conf.urls import url, include
from . import views
urlpatterns = [
	url(r'^users/$', views.UserList.as_view()),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
	url(r'^suppliers/$', views.SupplierList.as_view()),
	url(r'^suppliers/(?P<pk>[0-9]+)/$', views.SupplierDetail.as_view()),
	url(r'^itemtypes/$', views.ItemTypeList.as_view()),
	url(r'^itemtypes/(?P<pk>[0-9]+)/$', views.ItemTypeDetail.as_view()),
	url(r'^onsaleitems/$', views.OnSaleItemList.as_view()),
	url(r'^onsaleitems/(?P<pk>[0-9]+)/$', views.OnSaleItemDetail.as_view()),
]