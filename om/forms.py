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

class _OrderForm(forms.ModelForm):
	company = forms.ModelChoiceField(
		queryset=Company.objects.filter(is_supplier=True),
		widget=forms.TextInput
	)
	
	class Meta:
		model = models.Order

class OrderForm(forms.ModelForm):
	company = forms.ModelChoiceField(
		queryset=Company.objects.filter(is_supplier=True),
		widget=forms.HiddenInput
	)
	items = forms.ModelMultipleChoiceField(
		queryset=models.CartItem.objects.all()
	)
	notes = forms.CharField(
		required=False,
		widget=forms.Textarea
	)

	class Meta:
		model = models.Order
	
class OrderItemReceptionForm(forms.ModelForm):
	receive = forms.IntegerField(required=False)
	estimated_delivery = forms.DateField(required=False,
		input_formats=['%d/%m/%Y', '%Y-%m-%d'],
		widget=forms.TextInput(attrs={"class": "dateinput"})
	)
	
	class Meta:
		fields = ['estimated_delivery',]

