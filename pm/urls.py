from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from pm.models import Sector, Project, Machine, MachineComment
from pm.views import MachinePartsView

urlpatterns = patterns("pm.views",
    url(r'^$',
		ListView.as_view(
			model=Project,
        	paginate_by=10,
			context_object_name="project_list"
		),
		name="pm_project_list"
	),
	url(r'^sector/list/$',
		ListView.as_view(
			model=Sector,
			paginate_by=10,
			context_object_name="sector_list"
		),
		name="pm_sector_list"
	),
	url(r'^sector/detail/(?P<pk>\d+)/$',
		DetailView.as_view(
			model=Sector,
			context_object_name="sector"
		),
		name="pm_sector_detail"
	),
	url(r'^sector/edit/(?P<pk>\d+)/$',
		UpdateView.as_view(
			model=Sector,
		),
		name="pm_sector_edit"
	),
	url(r'^sector/create/$',
		CreateView.as_view(
			model = Sector
		),
		name="pm_sector_create"
	),
    url(r'^project/detail/(?P<pk>\d+)/$',
		DetailView.as_view(
			model=Project,
        	context_object_name="project"
		),
		name="pm_project_detail"
	),
    url(r'^project/edit/(?P<pk>\d+)/$',
		UpdateView.as_view(
			model=Project,
		),
		name="pm_project_edit"
	),
	url(r'^project/create/$',
		CreateView.as_view(
			model=Project
		),
		name="pm_project_create"
	),
    url(r'^machine/detail/(?P<pk>\d+)/$',
		DetailView.as_view(
			model=Machine,
        	context_object_name="machine"
		),
		name="pm_machine_detail"
	),
    url(r'^machine/parts/(?P<pk>\d+)/$',
		MachinePartsView.as_view(),
		name="pm_machine_parts"
	),
    url(r'^machine/edit/(?P<pk>\d+)/$',
		UpdateView.as_view(
			model=Machine,
		),
		name="pm_machine_edit"
	),
    url(r'^machine/create/$',
		CreateView.as_view(
			model=Machine,
		),
		name="pm_machine_create"
	),
    url(r'^comment/create/$',
		CreateView.as_view(
			model=MachineComment,
		),
		name="pm_machinecomment_create"
	),
	url(r'^part/create/$', 'create_part', name="pm_part_create"),
)
