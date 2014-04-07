from datetime import date
from decimal import *
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden 
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from indumatic.search import get_query
from indumatic.views import PdfView
from crm.defaults import *
from crm.models import *
from crm import forms
from pm.models import Project

class CompanyListView(ListView):
	model=Company
	paginate_by=10
	context_object_name="company_list"

	@method_decorator(permission_required('crm.view_company',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(CompanyListView, self).dispatch(*args, **kwargs)

class CompanyDetailView(DetailView):
	model=Company
	context_object_name="company"

	@method_decorator(permission_required('crm.view_company',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(CompanyDetailView, self).dispatch(*args, **kwargs)

class CompanyCreateView(CreateView):
	model = Company

	@method_decorator(permission_required('crm.add_company',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(CompanyCreateView, self).dispatch(*args, **kwargs)

class CompanyUpdateView(UpdateView):
	model = Company

	@method_decorator(permission_required('crm.change_company',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(CompanyUpdateView, self).dispatch(*args, **kwargs)

class CompanySearchView(ListView):
	model = Company
	context_object_name = 'company_list'
	template_name = 'crm/company_list.html'

	def get_queryset(self):
		query_string = self.request.GET.get('q', '')
		entry_query = get_query(query_string,
			['name', 'city', 'region', 'country',]
		)
		print entry_query
		found_entries = Company.objects.filter(entry_query)
		return found_entries

class DepartmentDetailView(DetailView):
	model=Department
	context_object_name="department"

	@method_decorator(permission_required('crm.view_department',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(DepartmentDetailView, self).dispatch(*args, **kwargs)

class DepartmentCreateView(CreateView):
	model = Department
	form_class = forms.DepartmentForm

	@method_decorator(permission_required('crm.add_department',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(DepartmentCreateView, self).dispatch(*args, **kwargs)

	def get_initial(self):
		return {'company': self.kwargs['pk']}

class DepartmentUpdateView(UpdateView):
	model = Department
	form_class = forms.DepartmentForm

	@method_decorator(permission_required('crm.change_department',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(DepartmentUpdateView, self).dispatch(*args, **kwargs)

class GroupListView(ListView):
	model=Group
	paginate_by=10
	context_object_name="group_list"

	@method_decorator(permission_required('crm.view_group',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(GroupListView, self).dispatch(*args, **kwargs)

class GroupDetailView(DetailView):
	model=Group
	context_object_name="group"

	@method_decorator(permission_required('crm.view_group',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(GroupDetailView, self).dispatch(*args, **kwargs)

class GroupUpdateView(UpdateView):
	model = Group
	
	@method_decorator(permission_required('crm.change_group',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(GroupUpdateView, self).dispatch(*args, **kwargs)

class GroupCreateView(CreateView):
	model = Group

	@method_decorator(permission_required('crm.add_group',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(GroupCreateView, self).dispatch(*args, **kwargs)

##
## QUOTATIONS VIEWS
##

def ip_unrestricted(ip):
	ip_list = ip.split(".", 3)[:3]
	for n in SAFE_NETWORKS:
		if n.split(".", 3)[:3] == ip_list:
			return True
	return False

class RestrictedNetworkMixin(object):
	def dispatch(self, *args, **kwargs):
		if ip_unrestricted(self.request.META['REMOTE_ADDR']):
			return super(RestrictedNetworkMixin, self).dispatch(*args, **kwargs)
		#return HttpResponseForbidden()
		raise PermissionDenied()

class QuotationListView(ListView):
	model = Quotation
	paginate_by = 20

	@method_decorator(permission_required('crm.view_quotation',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(QuotationListView, self).dispatch(*args, **kwargs)

class CompanyQuotationListView(QuotationListView):
	def get_queryset(self):
		return Quotation.objects.filter(company__id=self.kwargs['pk'])

class QuotationCreateView(RestrictedNetworkMixin, CreateView):
	model = Quotation
	form_class = forms.QuotationForm

	@method_decorator(permission_required('crm.add_quotation',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(QuotationCreateView, self).dispatch(*args, **kwargs)

	def get_initial(self):
		company = get_object_or_404(Company, id=self.kwargs['pk'])
		return {'company': company}

	def form_valid(self, form):
		q = form.save(commit=False)
		q.author = self.request.user
		q.save()
		return HttpResponseRedirect(q.get_absolute_url())

class QuotationUpdateView(RestrictedNetworkMixin, UpdateView):
	model = Quotation
	form_class = forms.QuotationForm

	@method_decorator(permission_required('crm.change_quotation',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(QuotationUpdateView, self).dispatch(*args, **kwargs)

class QuotationDetailView(RestrictedNetworkMixin, DetailView):
	model = Quotation
	
	@method_decorator(permission_required('crm.view_quotation',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(QuotationDetailView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx = super(QuotationDetailView, self).get_context_data(**kwargs)
		form_class = forms.quotationitem_form_factory(
			with_price=self.object.disaggregated
		)
		ctx.update({
			'form': form_class(initial={'quotation': self.object, }),
		})
		return ctx

class QuotationItemCreateView(RestrictedNetworkMixin, CreateView):
	model = QuotationItem

	@method_decorator(permission_required('crm.add_quotationitem',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(QuotationItemCreateView, self).dispatch(*args, **kwargs)

	def get_form_class(self):
		return forms.quotationitem_form_factory()

	def get_success_url(self):
		return self.object.quotation.get_absolute_url()

class QuotationItemUpdateView(RestrictedNetworkMixin, UpdateView):
	model = QuotationItem

	@method_decorator(permission_required('crm.change_quotationitem',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(QuotationItemUpdateView, self).dispatch(*args, **kwargs)

	def get_form_class(self):
		return forms.quotationitem_form_factory(
			with_price=self.object.quotation.disaggregated
		)

	def get_success_url(self):
		return self.object.quotation.get_absolute_url()

class QuotationItemDeleteView(RestrictedNetworkMixin, DeleteView):
	model = QuotationItem

	@method_decorator(permission_required('crm.delete_quotationitem',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(QuotationItemDeleteView, self).dispatch(*args, **kwargs)

	def get_success_url(self):
		return self.object.quotation.get_absolute_url()

class QuotationPdfView(RestrictedNetworkMixin, PdfView):

	@method_decorator(permission_required('crm.view_quotation',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		self.object = get_object_or_404(Quotation, id=self.kwargs['pk'])
		return super(QuotationPdfView, self).dispatch(*args, **kwargs)

	def get_template_names(self):
		return ['crm/quotation_%s_pdf.html' % self.object.language,]

	def get_context_data(self, **kwargs):
		ctx = super(QuotationPdfView, self).get_context_data(**kwargs)
		quotation = self.object
		if quotation.disaggregated:
			total = 0
			for item in quotation.quotationitem_set.non_optional().with_total():
				total += item.total
		else:
			total = quotation.total
		ctx.update({
			'quotation': quotation,
			'address': COMPANY_ADDRESS,
			'city': COMPANY_CITY,
			'options': quotation.quotationitem_set.optional().count() > 0,
			'total': total,
		})
		return ctx

##
## CONTRACT VIEWS
##

class ContractListView(ListView):
	model = Contract
	paginate_by = 20

	@method_decorator(permission_required('crm.view_contract',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(ContractListView, self).dispatch(*args, **kwargs)

class CompanyContractListView(ContractListView):
	def get_queryset(self):
		return Contract.objects.filter(company__id=self.kwargs['pk'])

class ContractCreateView(RestrictedNetworkMixin, CreateView):
	model = Contract
	form_class = forms.ContractForm

	@method_decorator(permission_required('crm.add_contract',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(ContractCreateView, self).dispatch(*args, **kwargs)

	def get_initial(self):
		company = get_object_or_404(Company, id=self.kwargs['pk'])
		return {'company': company}

	def form_valid(self, form):
		q = form.save(commit=False)
		q.author = self.request.user
		q.save()
		return HttpResponseRedirect(q.get_absolute_url())

class ContractUpdateView(RestrictedNetworkMixin, UpdateView):
	model = Contract
	form_class = forms.ContractForm

	@method_decorator(permission_required('crm.change_contract',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(ContractUpdateView, self).dispatch(*args, **kwargs)

class ContractSignedCopyUpload(ContractUpdateView):
	form_class = forms.ContractSignedCopyForm

class ContractDetailView(RestrictedNetworkMixin, DetailView):
	model = Contract
	
	@method_decorator(permission_required('crm.view_contract',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(ContractDetailView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx = super(ContractDetailView, self).get_context_data(**kwargs)
		form_class = forms.contractitem_form_factory(
			with_price=self.object.disaggregated
		)
		ctx.update({
			'form': form_class(initial={'contract': self.object, }),
			'MEDIA_URL': settings.MEDIA_URL,
		})
		return ctx

class ContractItemCreateView(RestrictedNetworkMixin, CreateView):
	model = ContractItem

	@method_decorator(permission_required('crm.add_contractitem',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(ContractItemCreateView, self).dispatch(*args, **kwargs)

	def get_form_class(self):
		return forms.contractitem_form_factory()

	def get_success_url(self):
		return self.object.contract.get_absolute_url()

class ContractItemUpdateView(RestrictedNetworkMixin, UpdateView):
	model = ContractItem

	@method_decorator(permission_required('crm.change_contractitem',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(ContractItemUpdateView, self).dispatch(*args, **kwargs)

	def get_form_class(self):
		return forms.contractitem_form_factory(
			with_price=self.object.contract.disaggregated
		)

	def get_success_url(self):
		return self.object.contract.get_absolute_url()

class ContractItemDeleteView(RestrictedNetworkMixin, DeleteView):
	model = ContractItem

	@method_decorator(permission_required('crm.delete_contractitem',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(ContractItemDeleteView, self).dispatch(*args, **kwargs)

	def get_success_url(self):
		return self.object.contract.get_absolute_url()

class ContractPdfView(RestrictedNetworkMixin, PdfView):

	@method_decorator(permission_required('crm.view_contract',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		self.object = get_object_or_404(Contract, id=self.kwargs['pk'])
		return super(ContractPdfView, self).dispatch(*args, **kwargs)

	def get_template_names(self):
		return ['crm/contract_%s_pdf.html' % self.object.language,]

	def get_context_data(self, **kwargs):
		ctx = super(ContractPdfView, self).get_context_data(**kwargs)
		contract = self.object
		if contract.disaggregated:
			total = 0
			for item in contract.contractitem_set.with_total():
				total += item.total
		else:
			total = contract.total
		total = Decimal(total)
		vat_amount = total * contract.vat / 100
		vat_amount = vat_amount.quantize(Decimal('1.00'))
		ctx.update({
			'contract': contract,
			'address': COMPANY_ADDRESS,
			'city': COMPANY_CITY,
			'total': total,
			'vat_amount': vat_amount,
			'total_plus_vat': total + vat_amount,
		})
		return ctx

class QuotationToContractView(RestrictedNetworkMixin, RedirectView):
	http_method_names = ['post',]

	@method_decorator(permission_required('crm.add_contract',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(QuotationToContractView, self).dispatch(*args, **kwargs)

	def get_redirect_url(self, *args, **kwargs):
		quotation = get_object_or_404(Quotation, id=self.kwargs['pk'])
		try:
			contract = Contract.objects.create(
				company = quotation.company,
				author = self.request.user,
				created = date.today(),
				language = quotation.language,
				disaggregated = quotation.disaggregated,
				total = quotation.total,
				vat = 0)
		except Exception as e:
			messages.error(self.request,
				_("The contract could not be created. %s" % e)
			)
			return quotation.get_absolute_url()
		else:
			for item in quotation.quotationitem_set.non_optional():
				contract.contractitem_set.create(
					quantity = item.quantity,
					description = item.description,
					price = item.price
				)
			return contract.get_absolute_url()

class DeliveryNoteListView(ListView):
	model = DeliveryNote
	paginate_by = 20

	@method_decorator(permission_required('crm.view_deliverynote',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(DeliveryNoteListView, self).dispatch(*args, **kwargs)

class CompanyDeliveryNoteListView(DeliveryNoteListView):
	def get_queryset(self):
		return DeliveryNote.objects.filter(
			contract__company__id=self.kwargs['pk']
		)

class DeliveryNoteCreateView(FormView):
	template_name = 'crm/deliverynote_form.html'
	form_class = forms.DeliveryNoteForm
	
	@method_decorator(permission_required('crm.add_deliverynote',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		self.contract = get_object_or_404(Contract, id=self.kwargs['pk'])
		return super(DeliveryNoteCreateView, self).dispatch(*args, **kwargs)

	def get_form(self, form_class):
		return form_class(contract=self.contract, **self.get_form_kwargs())

	def form_valid(self, form):
		remarks = form.cleaned_data['remarks']
		items = form.cleaned_data['items']
		try:
			note = DeliveryNote.objects.create(
				contract = self.contract,
				remarks = remarks
			)
		except:
			messages.error(self.request,
				_("The delivery note could not be created.")
			)
			return HttpResponseRedirect(self.contract.get_absolute_url())
		else:
			for item in items:
				note.deliverynoteitem_set.create(
					quantity = item.quantity,
					description = item.description
				)
				## mark the machine as shipped
				item.machine_set.update(shipped_on=date.today())
		return HttpResponseRedirect(note.get_absolute_url())

class DeliveryNoteDetailView(DetailView):
	model = DeliveryNote
	
	@method_decorator(permission_required('crm.view_deliverynote',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(DeliveryNoteDetailView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx = super(DeliveryNoteDetailView, self).get_context_data(**kwargs)
		ctx.update({
			'form': forms.DeliveryNoteItemForm(
				initial={'note': self.object, }
					),
		})
		return ctx

class DeliveryNoteItemCreateView(CreateView):
	model = DeliveryNoteItem
	form_class = forms.DeliveryNoteItemForm

	@method_decorator(permission_required('crm.add_deliverynoteitem',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(DeliveryNoteItemCreateView, self).dispatch(*args, **kwargs)

	def get_success_url(self):
		return self.object.note.get_absolute_url()

class DeliveryNotePdfView(PdfView):

	@method_decorator(permission_required('crm.view_deliverynote',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		self.object = get_object_or_404(DeliveryNote, id=self.kwargs['pk'])
		return super(DeliveryNotePdfView, self).dispatch(*args, **kwargs)

	def get_template_names(self):
		return ['crm/delivery_%s_pdf.html' % self.object.contract.language,]

	def get_context_data(self, **kwargs):
		ctx = super(DeliveryNotePdfView, self).get_context_data(**kwargs)
		projects = Project.objects.filter(
			machine__contract_item__contract=self.object.contract
		).distinct()
		project_list = []
		for p in projects:
			project_list.append(unicode(p))
		ctx.update({
			'note': self.object,
			'address': COMPANY_ADDRESS,
			'projects': ", ".join(project_list),
		})
		return ctx

