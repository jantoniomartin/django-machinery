from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from crm.models import Company, Group, Department
from crm.views import *

urlpatterns = patterns("crm.views",
    url(r'^$',
		CompanyListView.as_view(),
		name="crm_company_list"
	),
	url(r'^group/list/$',
		GroupListView.as_view(),
		name="crm_group_list"
	),
	url(r'^group/detail/(?P<pk>\d+)/$',
		GroupDetailView.as_view(),
		name="crm_group_detail"
	),
	url(r'^group/edit/(?P<pk>\d+)/$',
		GroupUpdateView.as_view(),
		name="crm_group_edit"
	),
	url(r'^group/create/$',
		GroupCreateView.as_view(),
		name="crm_group_create"
	),
    url(r'^company/detail/(?P<pk>\d+)/$',
		CompanyDetailView.as_view(),
		name="crm_company_detail"
	),
    url(r'^company/edit/(?P<pk>\d+)/$',
		CompanyUpdateView.as_view(),
		name="crm_company_edit"
	),
	url(r'^company/create/$',
		CompanyCreateView.as_view(),
		name="crm_company_create"
	),
	url(r'^company/search/$',
		CompanySearchView.as_view(),
		name="crm_company_search"
	),
    url(r'^department/detail/(?P<pk>\d+)/$',
		DepartmentDetailView.as_view(),
		name="crm_department_detail"
	),
    url(r'^department/edit/(?P<pk>\d+)/$',
		DepartmentUpdateView.as_view(),
		name="crm_department_edit"
	),
    url(r'^company/add_department/(?P<pk>\d+)/$',
		DepartmentCreateView.as_view(),
		name="crm_department_create"
	),
)
