from django import forms

from wm.models import Article, Group

class ArticleForm(forms.ModelForm):
	group = forms.ModelChoiceField(queryset=Group.objects.all(),
		widget=forms.HiddenInput)
	
	class Meta:
		model = Article

class GroupForm(forms.ModelForm):
	parent = forms.ModelChoiceField(queryset=Group.objects.all(),
		widget=forms.HiddenInput)
	
	class Meta:
		model = Group
