from django.shortcuts import render

from indumatic.views import PdfView
from profiles.models import Employee

class EmployeeCodesView(PdfView):
    template_name = 'profiles/employee_codes.html'

    def get_context_data(self, **kwargs):
        ctx = super(EmployeeCodesView, self).get_context_data(**kwargs)
        employees = Employee.objects.all()
        ctx.update({ 'employees': employees})
        return ctx

