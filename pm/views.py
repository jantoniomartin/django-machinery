import json

from django.conf import settings
from django.contrib import messages
from django.core import serializers
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView

from pm.forms import *
from pm.models import Project, Machine, MachineComment, Part
from wm.models import Group
from indumatic.search import get_query
from indumatic.views import PdfView

class MachineCommentCreateView(CreateView):
	model = MachineComment
	
	def get_success_url(self):
		return self.object.machine.get_absolute_url()

class MachineCommentDeleteView(DeleteView):
	model = MachineComment
	
	def get_success_url(self):
		return self.object.machine.get_absolute_url()

class MachineDeleteView(DeleteView):
	model = Machine
	
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
	
	def get_success_url(self):
		return reverse_lazy('pm_machine_parts', args=[self.object.machine.id])

class PartUpdateView(UpdateView):
	model = Part
	form_class = PartForm

	def get_success_url(self):
		return reverse_lazy('pm_machine_parts', args=[self.object.machine.id])

class ProjectDetailView(DetailView):
	model = Project
	context_object_name = "project"
	
	def get_context_data(self, **kwargs):
		ctx = super(ProjectDetailView, self).get_context_data(**kwargs)
		machine_form = NewMachineForm(initial={'project': self.object.pk })
		ctx.update({ 'machine_form': machine_form,
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

	def get_queryset(self):
		query_string = self.request.GET.get('q', '')
		entry_query = get_query(query_string,
			['description',
			'machine__description',]
		)
		print entry_query
		found_entries = Project.objects.filter(entry_query)
		return found_entries

