from django import forms
from django.db.models import Max

from crm.models import Company
from pm.models import Project, Part

class ProjectForm(forms.ModelForm):
	company = forms.ModelChoiceField(queryset=Company.objects.filter(is_customer=True))

	class Meta:
		model = Project
		exclude = ['serial', 'old_model', 'is_retired']

	def save(self, force_insert=False, force_update=False, commit=True):
		m = super(ProjectForm, self).save(commit=False)
		if not m.serial:
			last_project = Project.objects.order_by("-serial")[0]
			n = int(last_project.serial)
			m.serial = str(n + 1).zfill(4)
		if commit:
			m.save()
		return m

class PartForm(forms.ModelForm):
	class Meta:
		model = Part
		fields = ['article', 'machine', 'quantity', 'function']
