import csv
from datetime import date
import json

from django.core import serializers
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import ObjectDoesNotExist, F
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from om.forms import OfferForm
from wm import models
from wm import forms
from indumatic.search import get_query

class GroupArticlesJSONView(TemplateView):
	def get(self, request, *args, **kwargs):
		try:
			group = models.Group.objects.get(id=kwargs['pk'])
		except ObjectDoesNotExist:
			raise Http404
		articles = group.article_set.order_by('code')
		to_json = []
		try:
			for article in articles:
				article_dict = {
					'pk': article.pk,
					'code': article.code,
					'brand': "&nbsp;",
					'description': article.description,
					'url': article.get_absolute_url(),
					'stock': article.stock,
					'unit': article.measure_unit,
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
		if self.template_name == 'wm/article_detail.html':
			latest_parts = self.object.part_set.all()[:10]
			offer_form = OfferForm(initial={"article": self.object.pk,})
			offers = self.object.offer_set.filter(expired_on__isnull=True)
			ctx.update({
				'latest_parts': latest_parts,
				'offer_form': offer_form,
				'offers': offers,
			})
		return ctx

class ArticleShortageView(ListView):
	model = models.Article
	template_object_name = "article_list"
	template_name = "wm/article_list"
	paginate_by = 10
	queryset = models.Article.objects.filter(
		control_stock=True,
		stock__lt=F('stock_alert')
	)

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

class StockReportView(View):
	def get(self, *args, **kwargs):
		nodes = models.Group.objects.all()
		response = HttpResponse(content_type="text/plain")
		response['Content-Disposition'] = 'attachment; filename="stock.csv"'
		w = csv.writer(response)
		for node in nodes:
			for a in node.article_set.all():
				if a.stock > 0:
					w.writerow([
						'"%s"' % a.code.encode('utf-8'),
						a.description.encode('utf-8'),
						a.measure_unit,
						getattr(a, 'brand', ''),
						a.stock,
					])
		return response

class ArticleSearchView(ListView):
	model = models.Article
	context_object_name = 'article_list'
	template_name = 'wm/article_list.html'

	def get_queryset(self):
		query_string = self.request.GET.get('q', '')
		entry_query = get_query(query_string,
			['code',
			'description',]
		)
		print entry_query
		found_entries = models.Article.objects.filter(entry_query)
		return found_entries

class SupplierCodeCreateView(CreateView):
	model = models.SupplierCode
	form_class = forms.SupplierCodeForm
	
	def get_initial(self):
		return {'article': self.kwargs['pk']}

	def get_success_url(self):
		return reverse('wm_scode_list', args=[self.kwargs['pk']])
		
class SupplierCodeEditView(UpdateView):
	model = models.SupplierCode
	form_class = forms.SupplierCodeForm
	
	def get_success_url(self):
		return reverse('wm_scode_list', args=[self.object.article.id])
		
class SupplierCodeDeleteView(DeleteView):
	model = models.SupplierCode
	
	def get_success_url(self):
		return reverse('wm_scode_list', args=[self.object.article.id])
		
