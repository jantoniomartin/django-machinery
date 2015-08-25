import datetime
import os

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.views.generic.base import TemplateView

from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse

import crm.models as crm
import om.models as om
import pm.models as pm
from indumatic.pdftools import make_pdf

class PermissionRequiredMixin(object):
	
	def dispatch(self, *args, **kwargs):
		if not self.request.user.has_perm(self.permission):
			raise PermissionDenied
		return super(PermissionRequiredMixin, self).dispatch(*args, **kwargs)

class PdfView(TemplateView):
	http_method_names = ['get',]

	def get_context_data(self, **kwargs):
		ctx = super(PdfView, self).get_context_data(**kwargs)
		ctx.update({'pagesize': 'A4'})
		return ctx

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		html = render_to_string(
			self.get_template_names(),
			context,
			context_instance=RequestContext(request)
		)
		try:
			document = make_pdf(html)
		except Exception as e:
			return HttpResponse(e.strerror)
		else:
			return HttpResponse(
				document.getvalue(),
				content_type="application/pdf"
			)

class DashboardView(TemplateView):
	template_name = "dashboard.html"

	def get_context_data(self, **kwargs):
		context = super(DashboardView, self).get_context_data(**kwargs)
		min_year = getattr(settings, "PM_RUNNING_ALL_BEFORE_YEAR", 1900)
		active_projects = pm.Project.objects.filter(
			is_retired=False,
            hide=False,
			machine__is_retired=False,
			machine__finished_on__isnull=True,
			machine__shipped_on__isnull=True,
			machine__running_on__isnull=True,
			machine__created_on__gt=datetime.date(min_year, 1, 1)
		).distinct()
		finished_projects = pm.Project.objects.filter(
			is_retired=False,
            hide=False,
			machine__is_retired=False,
			machine__finished_on__isnull=False,
			machine__running_on__isnull=True,
			machine__created_on__gt=datetime.date(min_year, 1, 1)
		).distinct()
		running_projects = pm.Project.objects.filter(
			is_retired=False,
            hide=False,
			machine__is_retired=False,
			machine__running_on__isnull=False).order_by(
				'-machine__running_on').distinct()[0:5]
		days = datetime.timedelta(14)
		delay = datetime.datetime.now() - days
		delayed_orderitems = om.OrderItem.objects.filter(
			completed_on__isnull=True,
			order__created_at__lt=delay
		).exclude(
			estimated_delivery__gte = datetime.datetime.today()
		).values_list('order__id', flat=True)
		delayed_orders = om.Order.objects.filter(id__in = delayed_orderitems)
		suppliers_in_cart = crm.Company.objects.filter(
			offer__cartitem__quantity__gt=0
		).distinct()
		pending_companies = crm.Company.objects.filter(
			order__orderitem__ordered_quantity__gt=0,	
			order__orderitem__completed_on__isnull=True
		).distinct()
		open_tickets = pm.Ticket.objects.exclude(status=2)
		comments = pm.MachineComment.objects.order_by('-created_on')[0:5]
		
		context.update({
			'active_projects': active_projects,
			'finished_projects': finished_projects,
			'running_projects': running_projects,
			'delayed_orders': delayed_orders,
			'suppliers_in_cart': suppliers_in_cart,
			'pending_companies': pending_companies,
			'open_tickets': open_tickets,
			'comments': comments,
			'MEDIA_URL': settings.MEDIA_URL,
		})
		return context

