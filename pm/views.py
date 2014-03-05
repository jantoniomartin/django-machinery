import json

from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.views.generic import DetailView

from pm.forms import NewMachineForm, PartForm
from pm.models import Project, Machine
from wm.models import Group

class MachinePartsView(DetailView):
	model=Machine
	context_object_name="machine"
	template_name="pm/machine_parts.html"

	def get_context_data(self, **kwargs):
		ctx = super(MachinePartsView, self).get_context_data(**kwargs)
		ctx.update({'nodes': Group.objects.all()})
		return ctx

class ProjectDetailView(DetailView):
	model = Project
	context_object_name = "project"
	
	def get_context_data(self, **kwargs):
		ctx = super(ProjectDetailView, self).get_context_data(**kwargs)
		machine_form = NewMachineForm(initial={'project': self.object.pk })
		ctx.update({ 'machine_form': machine_form })
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

