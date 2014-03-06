from django import forms

from om import models
from crm.models import Company
from wm.models import Article

class OfferForm(forms.ModelForm):
	article = forms.ModelChoiceField(queryset=Article.objects.all(),
		widget=forms.HiddenInput)
	company = forms.ModelChoiceField(
		queryset=Company.objects.filter(is_supplier=True)
	)
	confirmed_on = forms.DateField(required=False,
		input_formats=['%d/%m/%Y', '%Y-%m-%d'],
		widget=forms.DateInput(attrs={'class': 'dateinput'}))
	expired_on = forms.DateField(required=False,
		input_formats=['%d/%m/%Y', '%Y-%m-%d'],
		widget=forms.DateInput(attrs={'class': 'dateinput'}))
	
	class Meta:
		model = models.Offer

