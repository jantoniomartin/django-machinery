from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from indumatic.search import get_query
from crm.models import *
from crm import forms

class DepartmentCreateView(CreateView):
	model = Department
	form_class = forms.DepartmentForm

	def get_initial(self):
		return {'company': self.kwargs['pk']}

class DepartmentUpdateView(UpdateView):
	model = Department
	form_class = forms.DepartmentForm

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

