from django.forms import ModelForm

from pm.models import Part

class PartForm(ModelForm):
	class Meta:
		model = Part
		fields = ['article', 'machine', 'quantity', 'function']
