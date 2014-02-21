from haystack import indexes
from crm.models import Company, Group

class CompanyIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	name = indexes.CharField(model_attr='name')

	def get_model(self):
		return Company

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.all()

class GroupIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	name = indexes.CharField(model_attr='name')

	def get_model(self):
		return Group

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.all()

