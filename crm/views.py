from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView

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
