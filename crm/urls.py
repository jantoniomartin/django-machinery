from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from crm.models import Company, Group, Department

urlpatterns = patterns("djinn_crm.views",
    url(r'^$',
		ListView.as_view(
			model=Company,
        	paginate_by=10,
			context_object_name="company_list"
		),
		name="crm_company_list"
	),
	url(r'^group/list/$',
		ListView.as_view(
			model=Group,
			paginate_by=10,
			context_object_name="group_list"
		),
		name="crm_group_list"
	),
	url(r'^group/detail/(?P<pk>\d+)/$',
		DetailView.as_view(
			model=Group,
			context_object_name="group"
		),
		name="crm_group_detail"
	),
	url(r'^group/edit/(?P<pk>\d+)/$',
		UpdateView.as_view(
			model=Group,
		),
		name="crm_group_edit"
	),
	url(r'^group/create/$',
		CreateView.as_view(
			model = Group
		),
		name="crm_group_create"
	),
    url(r'^company/detail/(?P<pk>\d+)/$',
		DetailView.as_view(
			model=Company,
        	context_object_name="company"
		),
		name="crm_company_detail"
	),
    url(r'^company/edit/(?P<pk>\d+)/$',
		UpdateView.as_view(
			model=Company,
		),
		name="crm_company_edit"
	),
	url(r'^company/create/$',
		CreateView.as_view(
			model=Company
		),
		name="crm_company_create"
	),
    url(r'^department/detail/(?P<pk>\d+)/$',
		DetailView.as_view(
			model=Department,
        	context_object_name="department"
		),
		name="crm_department_detail"
	),
    url(r'^department/edit/(?P<pk>\d+)/$',
		UpdateView.as_view(
			model=Department,
		),
		name="crm_department_edit"
	),
	url(r'^department/create/$',
		CreateView.as_view(
			model=Department
		),
		name="crm_department_create"
	),
)
