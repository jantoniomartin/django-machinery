from django import forms

from crm.models import Department, Company

class DepartmentForm(forms.ModelForm):
	company = forms.ModelChoiceField(queryset=Company.objects.all(),
		widget=forms.HiddenInput)
	comment = forms.CharField(
		required=False,
		widget=forms.Textarea
	)


	class Meta:
		model = Department
