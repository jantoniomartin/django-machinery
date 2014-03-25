from django import forms
from django.utils.translation import ugettext_lazy as _

from wm.models import Article, Group, SupplierCode

class ArticleForm(forms.ModelForm):
	group = forms.ModelChoiceField(queryset=Group.objects.all(),
		widget=forms.HiddenInput)
	
	class Meta:
		exclude = ['documents',]
		model = Article

class DocumentLinkForm(forms.Form):
	article = forms.ModelChoiceField(queryset=Article.objects.all(),
		widget=forms.HiddenInput)
	uuid = forms.CharField(label="uuid",
		help_text=_("Paste the uuid of the document.")
		)

class GroupForm(forms.ModelForm):
	parent = forms.ModelChoiceField(queryset=Group.objects.all(),
		widget=forms.HiddenInput)
	
	class Meta:
		model = Group

class SupplierCodeForm(forms.ModelForm):
	article = forms.ModelChoiceField(queryset=Article.objects.all(),
		widget=forms.HiddenInput)
	
	class Meta:
		model = SupplierCode
