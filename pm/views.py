import json

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

## Libraries to generate pdf files
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string

from pm.forms import NewMachineForm, PartForm, MachineCommentForm
from pm.models import Project, Machine, MachineComment, Part
from wm.models import Group

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
		ctx.update({'nodes': Group.objects.all()})
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

def make_pdf(html):
	""" Make the pdf file and return it as HttpResponse """
	result = StringIO.StringIO()
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type="application/pdf")
	return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

class PdfView(TemplateView):
	http_method_names = ['get',]

	def get_context_data(self, **kwargs):
		ctx = super(PdfView, self).get_context_data(**kwargs)
		ctx.update({'pagesize': 'A4'})
		return ctx

	def make_pdf(self, html):
		""" Make the pdf file and return it as HttpResponse """
		result = StringIO.StringIO()
		pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
		if not pdf.err:
			response = HttpResponse(
				result.getvalue(),
				content_type="application/pdf"
			)
			#response['Content-Disposition'] = 'attachment; filename="some.pdf"'
			return response
		return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		html = render_to_string(
			self.template_name,
			context,
			context_instance=RequestContext(request)
		)
		return self.make_pdf(html)

class PartsReportView(PdfView):
	template_name = 'pm/parts_pdf.html'

	def get_context_data(self, **kwargs):
		ctx = super(PartsReportView, self).get_context_data(**kwargs)
		project = get_object_or_404(Project, id=self.kwargs['pk'])
		ctx.update({ 'project': project})
		return ctx
