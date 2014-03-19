from django.db import models
from django.utils.translation import ugettext_lazy as _

import wm.models as wm
import crm.models as crm

class Offer(models.Model):
	article = models.ForeignKey(wm.Article, verbose_name=_("article"))
	company = models.ForeignKey(crm.Company, verbose_name=_("company"))
	created_on = models.DateField(_("created on"), auto_now_add=True)
	confirmed_on = models.DateField(_("confirmed on"), null=True, blank=True)
	expired_on = models.DateField(_("expired on"), null=True, blank=True)
	code = models.CharField(_("offer code"), max_length=50, null=True, blank=True)
	retail_price = models.FloatField(_("retail price"), null=True, blank=True)
	invoice_price = models.FloatField(_("invoice price"), null=True, blank=True)

	class Meta:
		ordering = ["company", "-created_on"]
		verbose_name = _("offer")
		verbose_name_plural = _("offers")

	def __unicode__(self):
		return _("Offer for %s") % self.article

class Order(models.Model):
	created_at = models.DateTimeField(_("created at"), auto_now_add=True)
	completed_on = models.DateField(_("completed on"), null=True, blank=True)
	notes = models.CharField(_("notes"), max_length=255, null=True, blank=True)
	company = models.ForeignKey(crm.Company, verbose_name=_("company"))

	class Meta:
		ordering = ["-id",]
		verbose_name = _("order")
		verbose_name_plural = _("orders")

	def __unicode__(self):
		return u"%(year)s-%(company)s-%(id)s" % {
			"year": self.created_at.strftime("%y"),
			"company": self.company.id,
			"id": self.id
		}

	@models.permalink
	def get_absolute_url(self):
		return ("om_order_detail", [self.id])

	@property
	def recipient_list(self):
		return self.company.department_set.filter(
			email__isnull=False,
			send_orders=True
		).values_list('email', flat=True)

class OrderItem(models.Model):
	ordered_quantity = models.FloatField(_("ordered quantity"))
	received_quantity = models.FloatField(_("received quantity"), default=0)
	completed_on = models.DateField(_("completed on"), null=True, blank=True)
	estimated_delivery = models.DateField(_("estimated delivery"), null=True, blank=True)
	order = models.ForeignKey(Order, verbose_name=_("order"))
	offer = models.ForeignKey(Offer, verbose_name=_("offer"))

	class Meta:
		ordering = ['-id',]
		verbose_name = _("order line")
		verbose_name_plural = _("order lines")

	def __unicode__(self):
		return self.id

class CartItem(models.Model):
	offer = models.ForeignKey(Offer, verbose_name=_("offer"))
	quantity = models.FloatField(_("quantity"))

	class Meta:
		verbose_name = _("cart item")
		verbose_name_plural = _("cart items")

	def __unicode__(self):
		return self.id
	
