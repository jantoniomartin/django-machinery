from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from om.views import *
from om.models import Offer, CartItem, Order

urlpatterns = patterns("om.views",
	url(r'^$',
		ListView.as_view(
			model = Order,
			context_object_name = "order_list",
			paginate_by = 10,
		),
		name="om_order_list"
	),
	url(r'^offer/create/$',
		OfferCreateView.as_view(),
		name="om_offer_create"
	),
	url(r'^offer/edit/(?P<pk>\d+)$',
		OfferUpdateView.as_view(),
		name="om_offer_edit"
	),
	url(r'^cartitem/create/$',
		CartItemCreateView.as_view(),
		name="om_cartitem_create"
	),
	url(r'^cartitem/list/$',
		ListView.as_view(
			model = CartItem,
			context_object_name = "item_list",
		),
		name="om_cartitem_list"
	),
	url(r'^cartitem/delete/(?P<pk>\d+)$',
		DeleteView.as_view(
			model = CartItem,
			success_url = '/om/cartitem/list/',
		),
		name="om_cartitem_delete"
	),
	url(r'^order/create/(?P<pk>\d+)$',
		OrderCreateView.as_view(),
		name="om_order_create"
	),
	url(r'^order/detail/(?P<pk>\d+)$',
		OrderDetailView.as_view(),
		name="om_order_detail"
	),
)
