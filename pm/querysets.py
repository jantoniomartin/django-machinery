from django.db import models

class MachineQuerySet(models.query.QuerySet):
	def with_cost(self):
		return self.extra(select = {
			'total_cost':
			"""
			SELECT SUM(
				quantity * (SELECT MAX(invoice_price)
				FROM om_offer
				WHERE om_offer.article_id = pm_part.article_id)
			)
			FROM pm_part
			WHERE pm_part.machine_id = pm_machine.id
			"""
		})

class PartQuerySet(models.query.QuerySet):
	def with_cost(self):
		return self.extra(select = {
			'total_cost': """quantity * (SELECT MAX(invoice_price)
				FROM om_offer
				WHERE om_offer.article_id = pm_part.article_id)
				"""
		})
