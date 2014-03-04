import json

from django.core import serializers
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.generic import TemplateView

from wm import models

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
