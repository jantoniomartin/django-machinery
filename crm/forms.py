from django import forms
from django.utils.translation import ugettext_lazy as _

from crm.models import *

class DepartmentForm(forms.ModelForm):
	company = forms.ModelChoiceField(queryset=Company.objects.all(),
		widget=forms.HiddenInput)
	comment = forms.CharField(
		required=False,
		widget=forms.Textarea
	)


	class Meta:
		model = Department

class QuotationForm(forms.ModelForm):
	company = forms.ModelChoiceField(queryset=Company.objects.all(),
		widget=forms.HiddenInput)
	private_note = forms.CharField(required=False, label=_("Private note"),
		help_text=_("will not be shown in the document"),
		widget=forms.Textarea)

	class Meta:
		model = Quotation
		exclude = ['author',]

	def clean(self):
		cdata = super(QuotationForm, self).clean()
		if cdata['disaggregated'] and cdata['total'] is not None:
			raise forms.ValidationError(
				_("If the quotation is disaggregated, total must be empty.")
			)
		return cdata

def quotationitem_form_factory(with_price=True):
	class QuotationItemForm(forms.ModelForm):
		quotation = forms.ModelChoiceField(queryset=Quotation.objects.all(),
			widget=forms.HiddenInput)

		class Meta:
			model = QuotationItem
			if not with_price:
				exclude=['price']

	return QuotationItemForm

