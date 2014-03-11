import datetime
import os

from django.views.generic.base import TemplateView
from django.conf import settings

## Libraries to generate pdf files
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse

import crm.models as crm
import om.models as om
import pm.models as pm

def fetch_resources(uri, rel):
	sUrl = settings.STATIC_URL
	sRoot = settings.STATIC_ROOT
	mUrl = settings.MEDIA_URL
	mRoot = settings.MEDIA_ROOT
	if uri.startswith(mUrl):
		path = os.path.join(mRoot, uri.replace(mUrl, ""))
	elif uri.startswith(sUrl):
		path = os.path.join(sRoot, uri.replace(sUrl, ""))

	if not os.path.isfile(path):
		raise Exception(
			'media URI must start with %s or %s' % (sUrl, mUrl)
		)
	return path

class PdfView(TemplateView):
	http_method_names = ['get',]

	def get_context_data(self, **kwargs):
		ctx = super(PdfView, self).get_context_data(**kwargs)
		ctx.update({'pagesize': 'A4'})
		return ctx

	def make_pdf(self, html):
		""" Make the pdf file and return it as HttpResponse """
		result = StringIO.StringIO()
		pdf = pisa.pisaDocument(
			StringIO.StringIO(html.encode("UTF-8")),
			dest=result,
			link_callback=fetch_resources
		)
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

class DashboardView(TemplateView):
	template_name = "dashboard.html"

	def get_context_data(self, **kwargs):
		context = super(DashboardView, self).get_context_data(**kwargs)
		min_year = getattr(settings, "PM_RUNNING_ALL_BEFORE_YEAR", 1900)
		active_projects = pm.Project.objects.filter(
			machine__shipped_on__isnull=True,
			machine__running_on__isnull=True,
			machine__created_on__gt=datetime.date(min_year, 1, 1)
		).distinct()
		shipped_projects = pm.Project.objects.filter(
			machine__shipped_on__isnull=False,
			machine__running_on__isnull=True,
			machine__created_on__gt=datetime.date(min_year, 1, 1)
		).distinct()
		days = datetime.timedelta(14)
		delay = datetime.datetime.now() - days
		delayed_orders = om.Order.objects.filter(
			created_at__lt=delay,
			orderitem__completed_on__isnull=True
		).distinct()
		suppliers_in_cart = crm.Company.objects.filter(
			offer__cartitem__quantity__gt=0
		).distinct()
		pending_companies = crm.Company.objects.filter(
			order__orderitem__ordered_quantity__gt=0,	
			order__orderitem__completed_on__isnull=True
		).distinct()
		
		context.update({
			'active_projects': active_projects,
			'shipped_projects': shipped_projects,
			'delayed_orders': delayed_orders,
			'suppliers_in_cart': suppliers_in_cart,
			'pending_companies': pending_companies,
		})
		return context

