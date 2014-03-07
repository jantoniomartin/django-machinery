from datetime import date

from django.core.urlresolvers import reverse
from django.db.models import ObjectDoesNotExist
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from crm.models import Company
from om.models import *
from om import forms

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

	def get_success_url(self):
		return "/"

	def form_valid(self, form):
		order = form.save(commit=False)
		last_order = Order.objects.latest('reference')
		order.reference = last_order.reference + 1
		order.save()
		for item in form.cleaned_data["items"]:
			OrderItem.objects.create(
				order=order,
				ordered_quantity=item.quantity,
				offer=item.offer
			)
			item.delete()
		return HttpResponseRedirect(self.get_success_url())

class OrderDetailView(TemplateView):
	template_name = "om/order_detail.html"
	
	def get_formset_class(self):	
		return modelformset_factory(
			OrderItem,
			form=forms.OrderItemReceptionForm,
			extra=0
		)

	def get_context_data(self, *args, **kwargs):
		ctx = super(OrderDetailView, self).get_context_data(*args, **kwargs)
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
		for form in formset:
			if form.is_valid():
				receive = form.cleaned_data['receive']
				item = form.save(commit=False)
				if receive is not None:
					item.received_quantity += receive
					if item.received_quantity >= item.ordered_quantity:
						item.completed_on = date.today()
				item.save()
		## check if the order is completed

		return HttpResponseRedirect(
			reverse('om_order_detail', args=[self.kwargs['pk']])
		)
