from django import forms
from django.utils.translation import ugettext_lazy as _

from om import models
from crm.models import Company
from wm.models import Article

class OfferForm(forms.ModelForm):
	article = forms.ModelChoiceField(queryset=Article.objects.all(),
		widget=forms.HiddenInput)
	company = forms.ModelChoiceField(
		queryset=Company.objects.filter(is_supplier=True),
		label=_("Company")
	)
	expired_on = forms.DateField(required=False,
		input_formats=['%d/%m/%Y', '%Y-%m-%d'],
		label=_("Expiration"),
		widget=forms.DateInput(attrs={'class': 'dateinput'}))
	retail_price = forms.FloatField(localize=True, required=False,
		label = _("Retail price")
	)
	invoice_price = forms.FloatField(localize=True, required=False,
		label = _("Invoice price")
	)
	
	class Meta:
		model = models.Offer

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
	password = forms.CharField(label=_("Password"),
		widget=forms.PasswordInput)

	class Meta:
		model = models.Order
		exclude = ['completed_on', 'created_by',]

class OrderItemReceptionForm(forms.ModelForm):
	receive = forms.IntegerField(required=False)
	estimated_delivery = forms.DateField(required=False,
		input_formats=['%d/%m/%Y', '%Y-%m-%d'],
		widget=forms.TextInput(attrs={"class": "dateinput"})
	)
	retail_price = forms.FloatField(localize=True, required=False)
	invoice_price = forms.FloatField(localize=True, required=False)
	
	
	class Meta:
		fields = ['estimated_delivery',]

