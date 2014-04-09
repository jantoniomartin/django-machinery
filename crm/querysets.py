from django.db import models

class QuotationItemQuerySet(models.query.QuerySet):
	def with_total(self):
		return self.extra(
			select = {'total': 'quantity * price'}
		)
	
	def optional(self):
		return self.filter(optional=True)

	def non_optional(self):
		return self.exclude(optional=True)

class ContractItemQuerySet(models.query.QuerySet):
	def with_total(self):
		return self.extra(
			select = {'total': 'quantity * price'}
		)
	
class ProformaItemQuerySet(models.query.QuerySet):
	def with_total(self):
		return self.extra(
			select = {'total': 'quantity * price'}
		)
	
