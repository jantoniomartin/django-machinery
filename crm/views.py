from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from indumatic.search import get_query
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

