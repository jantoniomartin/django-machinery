from django.conf import settings
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from dm.models import *

class DocumentListView(ListView):
	model = Document
	paginate_by = 10

	def get_context_data(self, **kwargs):
		ctx = super(DocumentListView, self).get_context_data(**kwargs)
		ctx.update({
			'MEDIA_URL': settings.MEDIA_URL,
		})
		return ctx

class DocumentCreateView(CreateView):
	model = Document
	success_url = '/dm/'

class DocumentUpdateView(UpdateView):
	model = Document
	success_url = '/dm/'
