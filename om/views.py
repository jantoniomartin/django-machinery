from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView

from om.models import *
from om import forms

class OfferCreateView(CreateView):
	model = Offer
	form_class = forms.OfferForm

	def get_success_url(self):
		return self.object.article.get_absolute_url()

	def form_invalid(self, form):
		##TODO: improve this to show form errors
		id = self.request.POST['article']
		return HttpResponseRedirect(reverse('wm_article_detail', args=[id]))

class OfferUpdateView(UpdateView):
	model = Offer
	form_class = forms.OfferForm

	def get_success_url(self):
		return self.object.article.get_absolute_url()


