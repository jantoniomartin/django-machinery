from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from wm.models import Group, Article, SupplierCode
from wm.views import *

urlpatterns = patterns("wm.views",
	url(r'^$',
		ListView.as_view(
			model=Group,
			context_object_name="nodes",
			template_name="wm/group_tree.html"
		),
		name="wm_group_tree"
	),
	url(r'^article/list/$',
		ListView.as_view(
			model=Article,
			paginate_by=20,
			context_object_name="article_list"
		),
		name="wm_article_list"
	),
	url(r'^article/search/$',
		ArticleSearchView.as_view(),
		name="wm_article_search"
	),
	url(r'^article/shortage/$',
		ArticleShortageView.as_view(
	),
		name="wm_article_shortage"
	),
	url(r'^article/detail/(?P<pk>\d+)/$',
		ArticleDetailView.as_view(),
		name="wm_article_detail"
	),
	url(r'^article/offers/(?P<pk>\d+)/$',
		ArticleDetailView.as_view(
			template_name = 'wm/article_offers.html'
		),
		name="wm_article_offers"
	),
	url(r'^article/edit/(?P<pk>\d+)/$',
		ArticleUpdateView.as_view(),
		name="wm_article_edit"
	),
	url(r'^article/create/$',
		ArticleCreateView.as_view(),
		name="wm_article_create"
	),
	url(r'^group/create/$',
		GroupCreateView.as_view(),
		name="wm_group_create"
	),
	url(r'^group/edit/(?P<pk>\d+)/$',
		GroupUpdateView.as_view(),
		name="wm_group_edit"
	),
	url(r'^group/(?P<pk>\d+)/articles/$',
		GroupArticlesJSONView.as_view(),
		name="wm_group_articles"
	),
	url(r'^stock_report/$',
		StockReportView.as_view(),
		name="wm_stock_report"
	),
	url(r'^scodes/(?P<pk>\d+)/$',
		DetailView.as_view(
			model = Article,
			context_object_name = 'article',
			template_name = 'wm/article_supplier_codes.html'
		),
		name="wm_scode_list"
	),
	url(r'^scodes/(?P<pk>\d+)/create/$',
		SupplierCodeCreateView.as_view(),
		name="wm_scode_create"
	),
	url(r'^scodes/edit/(?P<pk>\d+)/$',
		SupplierCodeEditView.as_view(),
		name="wm_scode_edit"
	),
	url(r'^scodes/delete/(?P<pk>\d+)/$',
		SupplierCodeDeleteView.as_view(),
		name="wm_scode_delete"
	),
)
