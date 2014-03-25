from django.conf.urls import patterns, url

from dm.views import *

urlpatterns = patterns("dm.views",
	url(r'^$', DocumentListView.as_view(), name='dm_document_list'),
	url(r'^document/create/$',
		DocumentCreateView.as_view(),
		name='dm_document_create'
	),
	url(r'^document/edit/(?P<pk>\d+)/$',
		DocumentUpdateView.as_view(),
		name='dm_document_update'
	),
)
