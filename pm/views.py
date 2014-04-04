import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core import serializers
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView

from pm.forms import *
from pm.models import *
from wm.models import Group
from indumatic.search import get_query
from indumatic.views import PdfView

class MachineCommentCreateView(CreateView):
	model = MachineComment
	form_class = MachineCommentForm
	
	@method_decorator(permission_required('pm.add_machinecomment',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(MachineCommentCreateView, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		comment = form.save(commit = False)
		comment.author = self.request.user
		comment.save()
		return HttpResponseRedirect(comment.machine.get_absolute_url())

class MachineCommentDeleteView(DeleteView):
	model = MachineComment
	
	@method_decorator(permission_required('pm.delete_machinecomment',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(MachineCommentDeleteView, self).dispatch(*args, **kwargs)

	def get_success_url(self):
		return self.object.machine.get_absolute_url()

class MachineUpdateView(UpdateView):
	model=Machine
	form_class = MachineForm

	@method_decorator(permission_required('pm.change_machine',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(MachineUpdateView, self).dispatch(*args, **kwargs)

class MachineDeleteView(DeleteView):
	model = Machine
	
	@method_decorator(permission_required('pm.delete_machine',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(MachineDeleteView, self).dispatch(*args, **kwargs)

	def get_success_url(self):
		return self.object.project.get_absolute_url()

class MachineDetailView(DetailView):
	model = Machine
	context_object_name = "machine"

	def get_context_data(self, **kwargs):
		ctx = super(MachineDetailView, self).get_context_data(**kwargs)
		comment_form = MachineCommentForm(initial={'machine': self.object.pk })
		ctx.update({ 'comment_form': comment_form })
		return ctx

class MachinePartsView(DetailView):
	model=Machine
	context_object_name="machine"
	template_name="pm/machine_parts.html"

	def get_context_data(self, **kwargs):
		ctx = super(MachinePartsView, self).get_context_data(**kwargs)
		ctx.update({
			'nodes': Group.objects.all(),
			'import_form': MachineSelectForm(),
		})

		return ctx

class PartDeleteView(DeleteView):
	model = Part
	
	@method_decorator(permission_required('pm.delete_part',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(PartDeleteView, self).dispatch(*args, **kwargs)

	def get_success_url(self):
		return reverse_lazy('pm_machine_parts', args=[self.object.machine.id])

class PartUpdateView(UpdateView):
	model = Part
	form_class = PartForm

	@method_decorator(permission_required('pm.change_part',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(PartUpdateView, self).dispatch(*args, **kwargs)

	def get_success_url(self):
		return reverse_lazy('pm_machine_parts', args=[self.object.machine.id])

class ProjectCreateView(CreateView):
	model=Project
	form_class = ProjectForm

	@method_decorator(permission_required('pm.add_project',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(ProjectCreateView, self).dispatch(*args, **kwargs)

class ProjectUpdateView(CreateView):
	model=Project
	form_class = ProjectForm
	context_object_name = 'project'

	@method_decorator(permission_required('pm.change_project',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(ProjectUpdateView, self).dispatch(*args, **kwargs)

class ProjectDetailView(DetailView):
	model = Project
	context_object_name = "project"
	
	def get_context_data(self, **kwargs):
		ctx = super(ProjectDetailView, self).get_context_data(**kwargs)
		machine_form = NewMachineForm(initial={'project': self.object.pk })
		try:
			ce = CECertificate.objects.get(project=self.object)
		except ObjectDoesNotExist:
			ce = None
		ctx.update({ 'machine_form': machine_form,
					'ce': ce,
					'MEDIA_URL': settings.MEDIA_URL,})
		return ctx

class ProjectListView(ListView):
	model = Project
	context_object_name = "project_list"
	paginate_by = 10

	def get_context_data(self, **kwargs):
		ctx = super(ProjectListView, self).get_context_data(**kwargs)
		ctx.update({ 'MEDIA_URL': settings.MEDIA_URL })
		return ctx

class SectorCreateView(CreateView):
	model=Sector

	@method_decorator(permission_required('pm.add_sector',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(SectorCreateView, self).dispatch(*args, **kwargs)

class SectorUpdateView(CreateView):
	model=Sector

	@method_decorator(permission_required('pm.change_sector',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(SectorUpdateView, self).dispatch(*args, **kwargs)

@permission_required('pm.add_machine', raise_exception=True)
def create_machine(request):
	if not request.is_ajax():
		raise Http404
	if request.POST:
		form = NewMachineForm(request.POST)
		if form.is_valid():
			machine = form.save()
			machine_json = {
				"reference": unicode(machine),
				"description": machine.description,
				"created_on": machine.created_on.strftime("%d/%m/%Y"),
				"delivery": "",
				"detail_url": machine.get_absolute_url(),
				"edit_url": reverse('pm_machine_edit', args=[machine.id]),
				"delete_url": reverse('pm_machine_delete',
											args=[machine.id]),
			}
			if machine.estimated_delivery_on:
				print machine.estimated_delivery_on
				machine_json.update({
					"delivery": machine.estimated_delivery_on.strftime("%d/%m/%Y")
				})
			response_data = json.dumps(machine_json)
			return HttpResponse(response_data, content_type="application/json")
		else:
			errors_dict = {}
			if form.errors:
				for error in form.errors:
					e = form.errors[error]
					errors_dict[error] = unicode(e)
				return HttpResponseBadRequest(json.dumps(errors_dict))

@permission_required('pm.add_part', raise_exception=True)
def create_part(request):
	if not request.is_ajax():
		raise Http404
	if request.POST:
		form = PartForm(request.POST)
		if form.is_valid():
			part = form.save()
			part_json = {
				"quantity": part.quantity,
				"unit": part.article.measure_unit,
				"reference": part.article.code,
				"description": part.article.description,
				"function": part.function,
				"detail_url": part.article.get_absolute_url(),
				"edit_url": reverse('pm_part_edit', args=[part.id]),
				"delete_url": reverse('pm_part_delete', args=[part.id]),
			}
			response_data = json.dumps(part_json)
			return HttpResponse(response_data, content_type="application/json")
		else:
			errors_dict = {}
			if form.errors:
				for error in form.errors:
					e = form.errors[error]
					errors_dict[error] = unicode(e)
				return HttpResponseBadRequest(json.dumps(errors_dict))

def get_machine_ids(request, pk):
	if not request.is_ajax():
		raise Http404
	data = serializers.serialize("json", Machine.objects.filter(project__id=pk))
	return HttpResponse(data, content_type="application/json")

class CopyPartsView(FormView):
	template_name = 'pm/copy_parts.html'
	form_class = CopyPartsForm

	@method_decorator(permission_required('pm.add_part',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(CopyPartsView, self).dispatch(*args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CopyPartsView, self).get_form_kwargs()
		kwargs.update({
			"source_id": self.request.GET.get('machine_id', ''),
			#"initial": self.get_initial(),
		})
		return kwargs

	def get_initial(self):
		machine = get_object_or_404(Machine, id=self.kwargs['pk'])
		return {"machine_to": machine}

	def get_context_data(self, **kwargs):
		ctx = super(CopyPartsView, self).get_context_data(**kwargs)
		machine = get_object_or_404(Machine, id=self.kwargs['pk'])
		ctx.update({
			'machine': machine,
			'machine_from': self.request.GET.get('machine_id', ''),
		})
		return ctx

	def form_valid(self, form):
		parts = form.cleaned_data['parts']
		machine_to = form.cleaned_data['machine_to']
		n = 0
		for part in parts:
			Part.objects.create(
				article=part.article,
				machine=machine_to,
				quantity=part.quantity,
				function=part.function
			)
			n += 1
		messages.success(self.request,
			_("%s parts were successfully copied." % n))
		return HttpResponseRedirect(
			reverse('pm_machine_parts', args=[machine_to.id])
		)

class PartsReportView(PdfView):
	template_name = 'pm/parts_pdf.html'

	def get_context_data(self, **kwargs):
		ctx = super(PartsReportView, self).get_context_data(**kwargs)
		project = get_object_or_404(Project, id=self.kwargs['pk'])
		ctx.update({ 'project': project})
		return ctx

class ProjectSearchView(ListView):
	model = Project
	context_object_name = 'project_list'
	template_name = 'pm/project_list.html'

	def get_context_data(self, **kwargs):
		ctx = super(ProjectSearchView, self).get_context_data(**kwargs)
		ctx.update({ 'MEDIA_URL': settings.MEDIA_URL })
		return ctx

	def get_queryset(self):
		query_string = self.request.GET.get('q', '')
		entry_query = get_query(query_string,
			['serial',
			'description',
			'machine__description',]
		)
		print entry_query
		found_entries = Project.objects.filter(entry_query).distinct()
		return found_entries

class CECertificateCreateView(CreateView):
	model = CECertificate
	form_class = CECertificateForm
	template_name = 'pm/certificate_form.html'

	@method_decorator(permission_required('pm.add_cecertificate',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(CECertificateCreateView, self).dispatch(*args, **kwargs)

	def get_initial(self):
		return {'project': self.kwargs['pk'] }

	def get_success_url(self):
		return self.object.project.get_absolute_url()

class CECertificatePdfView(PdfView):
	template_name = 'ce_pdf.html'

	def get_context_data(self, **kwargs):
		ctx = super(CECertificatePdfView, self).get_context_data(**kwargs)
		certificate = get_object_or_404(CECertificate, id=self.kwargs['pk'])
		ctx.update({
			'cert': certificate,
		})
		return ctx
