import json

from django.contrib.auth.decorators import permission_required
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from indumatic.search import get_query
from indumatic.views import PdfView
from crm.defaults import *
from crm.models import *
from crm import forms

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

class QuotationCreateView(CreateView):
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

class QuotationUpdateView(UpdateView):
	model = Quotation
	form_class = forms.QuotationForm

	@method_decorator(permission_required('crm.change_quotation',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(QuotationUpdateView, self).dispatch(*args, **kwargs)

class QuotationDetailView(DetailView):
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

class QuotationItemCreateView(CreateView):
	model = QuotationItem

	@method_decorator(permission_required('crm.add_quotationitem',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(QuotationItemCreateView, self).dispatch(*args, **kwargs)

	def get_form_class(self):
		return forms.quotationitem_form_factory()

	def get_success_url(self):
		return self.object.quotation.get_absolute_url()

class QuotationItemUpdateView(UpdateView):
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

class QuotationItemDeleteView(DeleteView):
	model = QuotationItem

	@method_decorator(permission_required('crm.delete_quotationitem',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(QuotationItemDeleteView, self).dispatch(*args, **kwargs)

	def get_success_url(self):
		return self.object.quotation.get_absolute_url()

class QuotationPdfView(PdfView):

	@method_decorator(permission_required('crm.view_quotation',
		raise_exception=True))
	def dispatch(self, *args, **kwargs):
		self.object = get_object_or_404(Quotation, id=self.kwargs['pk'])
		return super(QuotationPdfView, self).dispatch(*args, **kwargs)

	def get_template_names(self):
		print "Looking for templates"
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
