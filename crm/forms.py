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

class ContractForm(forms.ModelForm):
	company = forms.ModelChoiceField(queryset=Company.objects.all(),
		widget=forms.HiddenInput)
	
	class Meta:
		model = Contract
		exclude = ['author', 'signed_copy',]

	def clean(self):
		cdata = super(ContractForm, self).clean()
		if cdata['disaggregated'] and cdata['total'] is not None:
			raise forms.ValidationError(
				_("If the quotation is disaggregated, total must be empty.")
			)
		return cdata

class ContractSignedCopyForm(forms.ModelForm):
	class Meta:
		model = Contract
		fields = ['signed_copy',]

def contractitem_form_factory(with_price=True):
	class ContractItemForm(forms.ModelForm):
		contract = forms.ModelChoiceField(queryset=Contract.objects.all(),
			widget=forms.HiddenInput)

		class Meta:
			model = ContractItem
			if not with_price:
				exclude=['price']

	return ContractItemForm

class ProformaForm(forms.ModelForm):
	company = forms.ModelChoiceField(queryset=Company.objects.all(),
		widget=forms.HiddenInput)
	
	class Meta:
		model = Proforma
		exclude = ['author',]

	def clean(self):
		cdata = super(ProformaForm, self).clean()
		if cdata['disaggregated'] and cdata['total'] is not None:
			raise forms.ValidationError(
				_("If the proforma is disaggregated, total must be empty.")
			)
		return cdata

def proformaitem_form_factory(with_price=True):
	class ProformaItemForm(forms.ModelForm):
		proforma = forms.ModelChoiceField(queryset=Proforma.objects.all(),
			widget=forms.HiddenInput)

		class Meta:
			model = ProformaItem
			if not with_price:
				exclude=['price']

	return ProformaItemForm

class DeliveryNoteForm(forms.Form):
	remarks = forms.CharField(required=False, label=_("Remarks"),
		widget=forms.Textarea)
	items = forms.ModelMultipleChoiceField(label=_("Composition"),
		queryset=ContractItem.objects.none(),
		widget=forms.CheckboxSelectMultiple)

	def __init__(self, *args, **kwargs):
		contract = kwargs.pop('contract')
		super(DeliveryNoteForm, self).__init__(*args, **kwargs)
		self.fields['items'].queryset = contract.contractitem_set.all()

	def clean(self):
		cleaned_data = super(DeliveryNoteForm, self).clean()
		for d in cleaned_data.values():
			print d
		return cleaned_data
	
class DeliveryNoteItemForm(forms.ModelForm):
	note = forms.ModelChoiceField(queryset=DeliveryNote.objects.all(),
		widget=forms.HiddenInput)

	class Meta:
		model = DeliveryNoteItem
