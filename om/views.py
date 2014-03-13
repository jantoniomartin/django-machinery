from datetime import date

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db.models import ObjectDoesNotExist
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, Context
from django.template.loader import render_to_string, get_template
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from crm.models import Company
from om.models import *
from om import forms
from indumatic.views import PdfView
from indumatic.pdftools import make_pdf

class CartItemCreateView(CreateView):
	model = CartItem
	success_url = "/"

	def form_valid(self, form):
		"""
		If the same offer is already in the cart, simply add the quantities.
		"""
		obj = form.save(commit=False)
		try:
			item = CartItem.objects.get(offer=obj.offer)
		except ObjectDoesNotExist:
			form.save(commit=True)
		else:
			item.quantity = item.quantity + obj.quantity
			item.save()
		return HttpResponseRedirect(obj.offer.article.get_absolute_url())

class OfferCreateView(CreateView):
	model = Offer
	form_class = forms.OfferForm

	def get_success_url(self):
		return self.object.article.get_absolute_url()

	def form_invalid(self, form):
		##TODO: improve this to show form errors
		id = self.request.POST['article']
		return HttpResponseRedirect(reverse('wm_article_detail', args=[id]))

class OfferUpdateView(UpdateView):
	model = Offer
	form_class = forms.OfferForm

	def get_success_url(self):
		return self.object.article.get_absolute_url()

class OrderCreateView(CreateView):
	form_class = forms.OrderForm
	template_name = "om/order_form.html"
	
	def get_initial(self):
		return {'company': self.kwargs['pk']}

	def get_context_data(self, **kwargs):
		ctx = super(OrderCreateView, self).get_context_data(**kwargs)
		supplier = get_object_or_404(Company, id=self.kwargs['pk'])
		items = CartItem.objects.filter(offer__company=supplier).extra(
			select={"cost": "om_offer.invoice_price*om_cartitem.quantity"}
		)
		ctx.update({
			'supplier': supplier,
			'items': items,
		})
		return ctx

	def form_valid(self, form):
		obj = form.save()
		for item in form.cleaned_data["items"]:
			OrderItem.objects.create(
				order=obj,
				ordered_quantity=item.quantity,
				offer=item.offer
			)
			item.delete()
		return HttpResponseRedirect(obj.get_absolute_url())

class OrderDetailView(DetailView):
	model = Order
	context_object_name = 'order'

	def get_subject_template(self):
		return get_template('om/order_subject.txt')

	def get_body_template(self):
		return get_template('om/order_body.txt')

	def post(self, request, *args, **kwargs):
		"""Send an email with the order report to the supplier."""
		self.object = self.get_object()
		ctx = self.get_context_data(**kwargs)
		ctx.update({'pagesize': 'A4'})
		items = OrderItem.objects.filter(order=self.object).extra(
			select={"cost": "select (om_offer.invoice_price*om_orderitem.ordered_quantity) from om_offer where om_offer.id=om_orderitem.offer_id"}
		)
		ctx.update({'items': items})
		html = render_to_string(
			'om/order_pdf.html',
			ctx,
			context_instance=RequestContext(request)
		)
		try:
			document = make_pdf(html)
		except Exception as e:
			if settings.DEBUG:
				return HttpResponse(e.strerror)
			else:
				messages.error(
					self.request,
					_("The pdf report for the order could not be made.")
				)
		else:
			subject = self.get_subject_template().render(Context(ctx))
			body = self.get_body_template().render(Context(ctx))
			message = EmailMessage(
				subject=subject.rstrip(),
				body=body,
				from_email='erp@indumatic.net',
				to=self.object.recipient_list,
				cc=['oficina.tecnica@indumatic.net',],
				attachments=[
					('%s.pdf' % self.object,
						document.getvalue(),
						'application/pdf'),
				],
				headers={'Reply-To': 'oficina.tecnica@indumatic.net'}
			)
			try:
				message.send()
			except Exception as e:
				messages.error(self.request, e)
			else:
				messages.success(self.request, _("The order was successfully sent."))
		return HttpResponseRedirect(reverse('om_order_pending'))

class OrderReceiveView(TemplateView):
	template_name = "om/order_receive.html"
	
	def get_formset_class(self):	
		return modelformset_factory(
			OrderItem,
			form=forms.OrderItemReceptionForm,
			extra=0
		)

	def get_context_data(self, *args, **kwargs):
		ctx = super(OrderReceiveView, self).get_context_data(*args, **kwargs)
		order = get_object_or_404(Order, id=self.kwargs['pk'])
		items = order.orderitem_set.extra(
			select={ 'pending': 'ordered_quantity - received_quantity' }
		)
		OrderItemFormSet = self.get_formset_class()
		formset = OrderItemFormSet(queryset=items)
		ctx.update({
			'order': order,
			'formset': formset,
		})
		return ctx

	def post(self, request, *args, **kwargs):
		order = get_object_or_404(Order, id=self.kwargs['pk'])
		OrderItemFormSet = self.get_formset_class()
		formset = OrderItemFormSet(self.request.POST)
		completed = True
		for form in formset:
			if form.is_valid():
				receive = form.cleaned_data['receive']
				item = form.save(commit=False)
				if receive is not None:
					item.received_quantity += receive
					if item.received_quantity >= item.ordered_quantity:
						item.completed_on = date.today()
					else:
						completed = False
				else:
					completed = False
				item.save()
		## mark the order as completed
		if completed:
			order.completed_on = date.today()
			order.save()

		return HttpResponseRedirect(
			reverse('om_order_receive', args=[self.kwargs['pk']])
		)

class OrderPdfView(PdfView):
	template_name = 'om/order_pdf.html'

	def get_context_data(self, *args, **kwargs):
		ctx = super(OrderPdfView, self).get_context_data(*args, **kwargs)
		order = get_object_or_404(Order, id=self.kwargs['pk'])
		items = OrderItem.objects.filter(order=order).extra(
			select={"cost": "select (om_offer.invoice_price*om_orderitem.ordered_quantity) from om_offer where om_offer.id=om_orderitem.offer_id"}
		)
		ctx.update({
			'order': order,
			'items': items,
		})
		return ctx

class OrderItemPendingView(ListView):
	model = OrderItem
	context_object_name = "item_list"
	paginate_by = 10
	template_name = 'om/orderitem_pending_list.html'
	
	def get_queryset(self):
		qs = OrderItem.objects.filter(completed_on__isnull=True)
		if 'pk' in self.kwargs.keys():
			qs = qs.filter(offer__company__id=self.kwargs['pk'])
		return qs
