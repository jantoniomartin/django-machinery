import json

from django.core import serializers
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from wm import models
from wm import forms

class GroupArticlesJSONView(TemplateView):
	def get(self, request, *args, **kwargs):
		try:
			group = models.Group.objects.get(id=kwargs['pk'])
		except ObjectDoesNotExist:
			raise Http404
		articles = group.article_set.all()
		to_json = []
		try:
			for article in articles:
				article_dict = {
					'pk': article.pk,
					'code': article.code,
					'brand': "&nbsp;",
					'description': article.description,
					'url': article.get_absolute_url(),
				}
				try:
					article_dict.update({'brand': article.brand.name })
				except:
					pass
				to_json.append(article_dict)
		except:
			raise Http404
		response_data = json.dumps(to_json)
		return HttpResponse(response_data, content_type='application/json')

class ArticleCreateView(CreateView):
	model = models.Article
	form_class = forms.ArticleForm

	def get_context_data(self, **kwargs):
		ctx = super(ArticleCreateView, self).get_context_data(**kwargs)
		nodes = models.Group.objects.all()
		ctx.update( {'nodes' : nodes })
		return ctx
		
class ArticleDetailView(DetailView):
	model = models.Article
	context_object_name = "article"

	def get_context_data(self, **kwargs):
		ctx = super(ArticleDetailView, self).get_context_data(**kwargs)
		latest_parts = self.object.part_set.all()[:10]
		ctx.update({ 'latest_parts': latest_parts })
		return ctx

class ArticleUpdateView(UpdateView):
	model = models.Article
	form_class = forms.ArticleForm

	def get_context_data(self, **kwargs):
		ctx = super(ArticleUpdateView, self).get_context_data(**kwargs)
		nodes = models.Group.objects.all()
		ctx.update( {'nodes' : nodes })
		return ctx
		
class GroupCreateView(CreateView):
	model = models.Group
	form_class = forms.GroupForm

	def get_context_data(self, **kwargs):
		ctx = super(GroupCreateView, self).get_context_data(**kwargs)
		nodes = models.Group.objects.all()
		ctx.update( {'nodes' : nodes })
		return ctx

	def get_success_url(self):
		return reverse('wm_group_tree')
		
class GroupUpdateView(UpdateView):
	model = models.Group
	context_object_name = "group"
	form_class = forms.GroupForm

	def get_context_data(self, **kwargs):
		ctx = super(GroupUpdateView, self).get_context_data(**kwargs)
		nodes = models.Group.objects.all()
		ctx.update( {'nodes' : nodes })
		return ctx
		
	def get_success_url(self):
		return reverse('wm_group_tree')
		
