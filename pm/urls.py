from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView

from pm.forms import ProjectForm, PartForm
from pm.models import *
from pm.views import *

urlpatterns = patterns("pm.views",
    url(r'^$',
		ProjectListView.as_view(),
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
		SectorUpdateView.as_view(),
		name="pm_sector_edit"
	),
	url(r'^sector/create/$',
		SectorCreateView.as_view(),
		name="pm_sector_create"
	),
    url(r'^project/detail/(?P<pk>\d+)/$',
		ProjectDetailView.as_view(),
		name="pm_project_detail"
	),
    url(r'^project/report/(?P<pk>\d+)/$',
		ProjectReportView.as_view(),
		name="pm_project_report"
	),
    url(r'^project/edit/(?P<pk>\d+)/$',
		ProjectUpdateView.as_view(),
		name="pm_project_edit"
	),
	url(r'^project/create/$',
		ProjectCreateView.as_view(),
		name="pm_project_create"
	),
	url(r'^project/search/$',
		ProjectSearchView.as_view(),
		name="pm_project_search"
	),
    url(r'^project/parts/report/(?P<pk>\d+)/$',
		PartsReportView.as_view(),
		name="pm_project_parts_report"
	),
    url(r'^project/parts/cost_report/(?P<pk>\d+)/$',
		PartsCostReportView.as_view(),
		name="pm_project_parts_costreport"
	),
    url(r'^project/ce/create/(?P<pk>\d+)/$',
		CECertificateCreateView.as_view(),
		name="pm_ce_certificate_create"
	),
    url(r'^ce/detail/(?P<pk>\d+)/$',
		CECertificatePdfView.as_view(),
		name="pm_ce_certificate_detail"
	),
    url(r'^machine/detail/(?P<pk>\d+)/$',
		MachineDetailView.as_view(),
		name="pm_machine_detail"
	),
    url(r'^machine/barcode/(?P<pk>\d+)/$',
		machine_barcode,
		name="pm_machine_barcode"
	),
    url(r'^machine/parts/(?P<pk>\d+)/$',
		MachinePartsView.as_view(),
		name="pm_machine_parts"
	),
    url(r'^machine/parts/report/(?P<pk>\d+)/$',
		MachinePartsReportView.as_view(),
		name="pm_machine_parts_report"
	),
    url(r'^machine/interventions/(?P<pk>\d+)/$',
		MachineInterventionsView.as_view(),
		name="pm_machine_interventions"
	),
    url(r'^machine/edit/(?P<pk>\d+)/$',
		MachineUpdateView.as_view(),
		name="pm_machine_edit"
	),
    url(r'^machine/delete/(?P<pk>\d+)/$',
		MachineDeleteView.as_view(),
		name="pm_machine_delete"
	),
	url(r'^machine/fromcontract/(?P<pk>\d+)/$',
		MachineFromContractItem.as_view(),
		name="pm_machine_from_contract_item"
	),
    url(r'^comment/create/$',
		MachineCommentCreateView.as_view(),
		name="pm_machinecomment_create"
	),
	url(r'^comment/delete/(?P<pk>\d+)/$',
		MachineCommentDeleteView.as_view(),
		name="pm_machinecomment_delete"
	),
	url(r'^part/edit/(?P<pk>\d+)/$',
		PartUpdateView.as_view(),
		name="pm_part_edit"
	),
	url(r'^part/delete/(?P<pk>\d+)/$',
		PartDeleteView.as_view(),
		name="pm_part_delete"
	),
	url(r'machine/copy_parts/(?P<pk>\d+)/',
		CopyPartsView.as_view(),
		name="pm_copy_parts"
	),
	url(r'^part/create/$', 'create_part', name="pm_part_create"),
	url(r'^machine/create/$', 'create_machine', name="pm_machine_create"),
	url(r'^machine_ids/(?P<pk>\d+)/$', 'get_machine_ids',name="pm_machine_ids"),
	url(r'^ticket/list/$',
		TicketListView.as_view(),
		name='pm_ticket_list'
	),
	url(r'^ticket/list/(?P<pk>\d+)/',
		ProjectTicketListView.as_view(),
		name='pm_project_ticket_list'
	),
	url(r'^ticket/detail/(?P<pk>\d+)/$',
		TicketDetailView.as_view(),
		name="pm_ticket_detail"
	),
	url(r'^ticket/status/(?P<pk>\d+)/$',
		TicketStatusUpdateView.as_view(),
		name="pm_ticket_status_update"
	),
    url(r'^ticket/create/(?P<pk>\d+)/$',
		TicketCreateView.as_view(),
		name="pm_ticket_create"
	),
    url(r'^ticketitem/create/$',
		TicketItemCreateView.as_view(),
		name="pm_ticketitem_create"
	),
    url(r'^intervention/create/(?P<pk>\d+)/$',
		InterventionCreateView.as_view(),
		name="pm_intervention_create"
	),
    url(r'^intervention/edit/(?P<pk>\d+)/$',
		InterventionUpdateView.as_view(),
		name="pm_intervention_update"
	),
    url(r'^intervention/import/$',
        import_interventions,
        name="pm_intervention_import"
    ),
)
