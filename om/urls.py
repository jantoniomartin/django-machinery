from django.conf.urls import patterns, url
from django.views.generic.edit import UpdateView

from om.views import *
from om.models import Offer

urlpatterns = patterns("om.views",
	url(r'^offer/create/$',
		OfferCreateView.as_view(),
		name="om_offer_create"
	),
	url(r'^offer/edit/(?P<pk>\d+)$',
		OfferUpdateView.as_view(),
		name="om_offer_edit"
	),
)
