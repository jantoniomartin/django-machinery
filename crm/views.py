from datetime import date
from decimal import *
import json

from django.conf import settings
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden 
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from indumatic.search import get_query
from indumatic.views import PermissionRequiredMixin, PdfView
from crm.defaults import *
from crm.models import *
from crm import forms
from pm.models import Project
from wm.models import Article

class CompanyListView(PermissionRequiredMixin, ListView):
	model=Company
	paginate_by=10
	context_object_name="company_list"
	permission = 'crm.view_company'

class CompanyDetailView(PermissionRequiredMixin, DetailView):
	model=Company
	context_object_name="company"
	permission = 'crm.view_company'

	def get_context_data(self, **kwargs):
		ctx = super(CompanyDetailView, self).get_context_data(**kwargs)
		ctx.update({
			'current_year': date.today().year, 
		})
		return ctx

class CompanyCreateView(PermissionRequiredMixin, CreateView):
	model = Company
	permission = 'crm.add_company'

class CompanyUpdateView(PermissionRequiredMixin, UpdateView):
	model = Company
	permission = 'crm.change_company'

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

class CompanyYearPurchase(ListView):
	template_name = 'crm/purchase_history.html'

	def get_queryset(self):
		return Article.objects.raw("""
			SELECT wm_article.*, SUM(om_orderitem.ordered_quantity) AS qty,
				YEAR(om_orderitem.completed_on) AS year
			FROM wm_article
			INNER JOIN om_offer
			ON om_offer.article_id = wm_article.id
				INNER JOIN om_orderitem
				ON om_orderitem.offer_id = om_offer.id
			WHERE om_offer.company_id = %(company)s
			AND YEAR(om_orderitem.completed_on) = %(year)s
			GROUP BY wm_article.code
			ORDER BY wm_article.code
		""" % {'company': self.kwargs['pk'],
				'year': self.kwargs['year'],
			}
		)
	
	def get_context_data(self, **kwargs):
		ctx = super(CompanyYearPurchase, self).get_context_data(**kwargs)
		company = get_object_or_404(Company, id=self.kwargs['pk'])
		ctx.update({
			'year': self.kwargs['year'],
			'previous_year': int(self.kwargs['year']) - 1,
			'next_year': int(self.kwargs['year']) + 1,
			'company': company,
		})
		return ctx

class DepartmentDetailView(PermissionRequiredMixin, DetailView):
	model=Department
	context_object_name="department"
	permission = 'crm.view_department'

class DepartmentCreateView(PermissionRequiredMixin, CreateView):
	model = Department
	form_class = forms.DepartmentForm
	permission = 'crm.add_department'

	def get_initial(self):
		return {'company': self.kwargs['pk']}

class DepartmentUpdateView(PermissionRequiredMixin, UpdateView):
	model = Department
	form_class = forms.DepartmentForm
	permission = 'crm.change_department'

class GroupListView(PermissionRequiredMixin, ListView):
	model=Group
	paginate_by=10
	context_object_name="group_list"
	permission = 'crm.view_group'

class GroupDetailView(PermissionRequiredMixin, DetailView):
	model=Group
	context_object_name="group"
	permission = 'crm.view_group'

class GroupUpdateView(PermissionRequiredMixin, UpdateView):
	model = Group
	permission = 'crm.change_group'

class GroupCreateView(PermissionRequiredMixin, CreateView):
	model = Group
	permission = 'crm.add_group'

##
## QUOTATIONS VIEWS
##

class QuotationListView(PermissionRequiredMixin, ListView):
	model = Quotation
	paginate_by = 20
	permission = 'crm.view_quotation'

class CompanyQuotationListView(QuotationListView):
	def get_queryset(self):
		return Quotation.objects.filter(company__id=self.kwargs['pk'])

class QuotationCreateView(PermissionRequiredMixin, CreateView):
	model = Quotation
	form_class = forms.QuotationForm
	permission = 'crm.add_quotation'

	def get_initial(self):
		company = get_object_or_404(Company, id=self.kwargs['pk'])
		return {'company': company}

	def form_valid(self, form):
		q = form.save(commit=False)
		q.author = self.request.user
		q.save()
		return HttpResponseRedirect(q.get_absolute_url())

class QuotationUpdateView(PermissionRequiredMixin, UpdateView):
	model = Quotation
	form_class = forms.QuotationForm
	permission = 'crm.change_quotation'

class QuotationDetailView(PermissionRequiredMixin, DetailView):
	model = Quotation
	permission = 'crm.view_quotation'
	
	def get_context_data(self, **kwargs):
		ctx = super(QuotationDetailView, self).get_context_data(**kwargs)
		form_class = forms.quotationitem_form_factory(
			with_price=self.object.disaggregated
		)
		ctx.update({
			'form': form_class(initial={'quotation': self.object, }),
		})
		return ctx

class QuotationItemCreateView(PermissionRequiredMixin, CreateView):
	model = QuotationItem
	permission = 'crm.add_quotationitem'

	def get_form_class(self):
		return forms.quotationitem_form_factory()

	def get_success_url(self):
		return self.object.quotation.get_absolute_url()

class QuotationItemUpdateView(PermissionRequiredMixin, UpdateView):
	model = QuotationItem
	permission = 'crm.change_quotationitem'

	def get_form_class(self):
		return forms.quotationitem_form_factory(
			with_price=self.object.quotation.disaggregated
		)

	def get_success_url(self):
		return self.object.quotation.get_absolute_url()

class QuotationItemDeleteView(PermissionRequiredMixin, DeleteView):
	model = QuotationItem
	permission = 'crm.delete_quotationitem'

	def get_success_url(self):
		return self.object.quotation.get_absolute_url()

class QuotationPdfView(PermissionRequiredMixin, PdfView):
	permission = 'crm.view_quotation'

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
			'disclaimer': DATA_DISCLAIMER,
		})
		return ctx

##
## CONTRACT VIEWS
##

class ContractListView(PermissionRequiredMixin, ListView):
	model = Contract
	paginate_by = 20
	permission = 'crm.view_contract'

class CompanyContractListView(ContractListView):
	def get_queryset(self):
		return Contract.objects.filter(company__id=self.kwargs['pk'])

class ContractCreateView(PermissionRequiredMixin, CreateView):
	model = Contract
	form_class = forms.ContractForm
	permission = 'crm.add_contract'

	def get_initial(self):
		company = get_object_or_404(Company, id=self.kwargs['pk'])
		return {'company': company}

	def form_valid(self, form):
		q = form.save(commit=False)
		q.author = self.request.user
		q.save()
		return HttpResponseRedirect(q.get_absolute_url())

class ContractUpdateView(PermissionRequiredMixin, UpdateView):
	model = Contract
	form_class = forms.ContractForm
	permission = 'crm.change_contract'

class ContractSignedCopyUpload(ContractUpdateView):
	form_class = forms.ContractSignedCopyForm

class ContractDetailView(PermissionRequiredMixin, DetailView):
	model = Contract
	permission = 'crm.view_contract'
	
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

class ContractItemCreateView(PermissionRequiredMixin, CreateView):
	model = ContractItem
	permission = 'crm.add_contractitem'

	def get_form_class(self):
		return forms.contractitem_form_factory()

	def get_success_url(self):
		return self.object.contract.get_absolute_url()

class ContractItemUpdateView(PermissionRequiredMixin, UpdateView):
	model = ContractItem
	permission = 'crm.change_contractitem'

	def get_form_class(self):
		return forms.contractitem_form_factory(
			with_price=self.object.contract.disaggregated
		)

	def get_success_url(self):
		return self.object.contract.get_absolute_url()

class ContractItemDeleteView(PermissionRequiredMixin, DeleteView):
	model = ContractItem
	permission = 'crm.delete_contractitem'

	def get_success_url(self):
		return self.object.contract.get_absolute_url()

class ContractPdfView(PermissionRequiredMixin, PdfView):
	permission = 'crm.view_contract'

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
			'disclaimer': DATA_DISCLAIMER,
		})
		return ctx

class QuotationToContractView(PermissionRequiredMixin, RedirectView):
	http_method_names = ['post',]
	permission = 'crm.add_contract'

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

##
## PROFORMA VIEWS
##

class ProformaListView(PermissionRequiredMixin, ListView):
	model = Proforma
	paginate_by = 20
	permission = 'crm.view_proforma'

class CompanyProformaListView(ProformaListView):
	def get_queryset(self):
		return Proforma.objects.filter(company__id=self.kwargs['pk'])

class ProformaCreateView(PermissionRequiredMixin, CreateView):
	model = Proforma
	form_class = forms.ProformaForm
	permission = 'crm.add_proforma'

	def get_initial(self):
		company = get_object_or_404(Company, id=self.kwargs['pk'])
		return {'company': company}

	def form_valid(self, form):
		q = form.save(commit=False)
		q.author = self.request.user
		q.save()
		return HttpResponseRedirect(q.get_absolute_url())

class ProformaUpdateView(PermissionRequiredMixin, UpdateView):
	model = Proforma
	form_class = forms.ProformaForm
	permission = 'crm.change_proforma'

class ProformaDetailView(PermissionRequiredMixin, DetailView):
	model = Proforma
	permission = 'crm.view_proforma'
	
	def get_context_data(self, **kwargs):
		ctx = super(ProformaDetailView, self).get_context_data(**kwargs)
		form_class = forms.proformaitem_form_factory(
			with_price=self.object.disaggregated
		)
		ctx.update({
			'form': form_class(initial={'proforma': self.object, }),
			'MEDIA_URL': settings.MEDIA_URL,
		})
		return ctx

class ProformaItemCreateView(PermissionRequiredMixin, CreateView):
	model = ProformaItem
	permission = 'crm.add_proformaitem'

	def get_form_class(self):
		return forms.proformaitem_form_factory()

	def get_success_url(self):
		return self.object.proforma.get_absolute_url()

class ProformaItemUpdateView(PermissionRequiredMixin, UpdateView):
	model = ProformaItem
	permission = 'crm.change_proformaitem'

	def get_form_class(self):
		return forms.proformaitem_form_factory(
			with_price=self.object.proforma.disaggregated
		)

	def get_success_url(self):
		return self.object.proforma.get_absolute_url()

class ProformaItemDeleteView(PermissionRequiredMixin, DeleteView):
	model = ProformaItem
	permission = 'crm.delete_proformaitem'

	def get_success_url(self):
		return self.object.proforma.get_absolute_url()

class ProformaPdfView(PermissionRequiredMixin, PdfView):
	permission = 'crm.view_proforma'

	def dispatch(self, *args, **kwargs):
		self.object = get_object_or_404(Proforma, id=self.kwargs['pk'])
		return super(ProformaPdfView, self).dispatch(*args, **kwargs)

	def get_template_names(self):
		return ['crm/proforma_%s_pdf.html' % self.object.language,]

	def get_context_data(self, **kwargs):
		ctx = super(ProformaPdfView, self).get_context_data(**kwargs)
		proforma = self.object
		if proforma.disaggregated:
			total = 0
			for item in proforma.proformaitem_set.with_total():
				total += item.total
		else:
			total = proforma.total
		total = Decimal(total)
		vat_amount = total * proforma.vat / 100
		vat_amount = vat_amount.quantize(Decimal('1.00'))
		ctx.update({
			'proforma': proforma,
			'address': COMPANY_ADDRESS,
			'city': COMPANY_CITY,
			'total': total,
			'vat_amount': vat_amount,
			'total_plus_vat': total + vat_amount,
			'disclaimer': DATA_DISCLAIMER,
		})
		return ctx

##
## DELIVERY NOTES VIEWS
##

class DeliveryNoteListView(ListView):
	model = DeliveryNote
	paginate_by = 20
	permission = 'crm.view_deliverynote'

class CompanyDeliveryNoteListView(DeliveryNoteListView):
	def get_queryset(self):
		return DeliveryNote.objects.filter(
			contract__company__id=self.kwargs['pk']
		)

class ContractDeliveryNoteListView(DeliveryNoteListView):
	def get_queryset(self):
		return DeliveryNote.objects.filter(
			contract__id=self.kwargs['pk']
		)

class DeliveryNoteCreateView(PermissionRequiredMixin, FormView):
	template_name = 'crm/deliverynote_form.html'
	form_class = forms.DeliveryNoteForm
	permission = 'crm.add_deliverynote'
	
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
				for machine in item.machine_set.all():
					if machine.shipped_on is None:
						machine.shipped_on = date.today()
						machine.save()
		return HttpResponseRedirect(note.get_absolute_url())

class DeliveryNoteDetailView(PermissionRequiredMixin, DetailView):
	model = DeliveryNote
	permission = 'crm.view_deliverynote'
	
	def get_context_data(self, **kwargs):
		ctx = super(DeliveryNoteDetailView, self).get_context_data(**kwargs)
		ctx.update({
			'form': forms.DeliveryNoteItemForm(
				initial={'note': self.object, }
					),
		})
		return ctx

class DeliveryNoteItemCreateView(PermissionRequiredMixin, CreateView):
	model = DeliveryNoteItem
	form_class = forms.DeliveryNoteItemForm
	permission = 'crm.add_deliverynoteitem'

	def get_success_url(self):
		return self.object.note.get_absolute_url()

class DeliveryNotePdfView(PermissionRequiredMixin, PdfView):
	permission = 'crm.view_deliverynote'

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

