from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from wm.models import Group, Article

urlpatterns = patterns("wm.views",
	url(r'^$',
		ListView.as_view(
			model=Article,
			paginate_by=20,
			context_object_name="article_list"
		),
		name="wm_article_list"
	),
	url(r'^article/detail/(?P<pk>\d+)/$',
		DetailView.as_view(
			model=Article,
			context_object_name="article"
		),
		name="wm_article_detail"
	),
	url(r'^article/edit/(?P<pk>\d+)/$',
		UpdateView.as_view(
			model=Article,
		),
		name="wm_article_edit"
	),
	url(r'^article/create/$',
		CreateView.as_view(
			model=Article
		),
		name="wm_article_create"
	),
	url(r'^group/detail/(?P<pk>\d+)/$',
		DetailView.as_view(
			model=Group,
			context_object_name="group"
		),
		name="wm_group_detail"
	),
)
