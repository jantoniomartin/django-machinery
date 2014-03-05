from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from pm.forms import ProjectForm
from pm.models import Sector, Project, Machine, MachineComment
from pm.views import *

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
		ProjectDetailView.as_view(),
		name="pm_project_detail"
	),
    url(r'^project/edit/(?P<pk>\d+)/$',
		UpdateView.as_view(
			model=Project,
			context_object_name = 'project',
			form_class = ProjectForm
		),
		name="pm_project_edit"
	),
	url(r'^project/create/$',
		CreateView.as_view(
			model=Project,
			form_class = ProjectForm
		),
		name="pm_project_create"
	),
    url(r'^machine/detail/(?P<pk>\d+)/$',
		MachineDetailView.as_view(),
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
    url(r'^machine/delete/(?P<pk>\d+)/$',
		MachineDeleteView.as_view(),
		name="pm_machine_delete"
	),
    url(r'^comment/create/$',
		MachineCommentCreateView.as_view(),
		name="pm_machinecomment_create"
	),
	url(r'^comment/delete/(?P<pk>\d+)/$',
		MachineCommentDeleteView.as_view(),
		name="pm_machinecomment_delete"
	),
	url(r'^part/create/$', 'create_part', name="pm_part_create"),
	url(r'^machine/create/$', 'create_machine', name="pm_machine_create"),
)
