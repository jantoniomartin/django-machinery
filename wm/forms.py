from django import forms
from django.utils.translation import ugettext_lazy as _

from wm.models import Article, Group, SupplierCode

class ArticleForm(forms.ModelForm):
	group = forms.ModelChoiceField(queryset=Group.objects.all(),
		widget=forms.HiddenInput)
	description = forms.CharField(
		label = _("Description"),
		widget=forms.Textarea)
	
	class Meta:
		exclude = ['documents', 'stock_updated',]
		model = Article

class ArticleBatchForm(forms.ModelForm):
    group = forms.CharField(widget=forms.HiddenInput)
    description = forms.CharField(
        label = _("Description"),
        widget=forms.Textarea(attrs={'rows': 2})
        )	

    class Meta:
        model = Article
        fields = ['group', 'code', 'description', 'measure_unit',
                'packaging', 'brand', 'stock', 'stock_value',]

class ArticleStockForm(forms.ModelForm):
    code = forms.CharField(widget=forms.HiddenInput)
    description = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Article
        fields = ['code', 'description', 'stock', 'stock_value',]

    def clean_code(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.code
        else:
            return self.cleaned_data['code']

    def clean_description(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.description
        else:
            return self.cleaned_data['description']

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
                fields = '__all__'

class SupplierCodeForm(forms.ModelForm):
	article = forms.ModelChoiceField(queryset=Article.objects.all(),
		widget=forms.HiddenInput)
	
	class Meta:
		model = SupplierCode
                fields = '__all__'
