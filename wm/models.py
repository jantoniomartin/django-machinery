from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from crm.models import Company
from dm.models import Document

class Brand(models.Model):
	name = models.CharField(_("name"), max_length=50)

	class Meta:
		ordering = ['name',]
		verbose_name = _("brand")
		verbose_name_plural = _("brands")

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return('wm_brand_detail', [self.id])

class Group(MPTTModel):
	name = models.CharField(_("name"), max_length=50)
	parent = TreeForeignKey('self', null=True, blank=True,
		related_name='children')

	class MPTTMeta:
		order_insertion_by = ['name']
	
	class Meta:
		verbose_name = _("group")
		verbose_name_plural = _("groups")

	def __unicode__(self):
		return self.name
	
	@models.permalink
	def get_absolute_url(self):
		return('wm_group_detail', [self.id])

@receiver(post_save, sender=Group)
def clear_tree_cache(sender, instance, created, raw, using, **kwargs):
	key = make_template_fragment_key('groups_tree', [])
	if cache.get(key):
		cache.delete(key)

class Article(models.Model):
	code = models.CharField(_("code"), max_length=128)
	description = models.CharField(_("description"), max_length=255)
	measure_unit = models.CharField(_("measure unit"), max_length=10,
		blank=True, null=True)
	packaging = models.PositiveIntegerField(_("standard packaging"), default=1)
	enabled = models.BooleanField(_("enabled"), default=True)
	favorited = models.BooleanField(_("favorited"), default=False)
	brand = models.ForeignKey(Brand, verbose_name=_("brand"), null=True, blank=True)
        weight = models.FloatField(_("weight (kg)"), default=0)
	group = models.ForeignKey(Group, verbose_name=_("group"))
	control_stock = models.BooleanField(_("control stock"), default=False)
	stock = models.PositiveIntegerField(_("stock"), default=0)
	stock_alert = models.PositiveIntegerField(_("stock alert"), default=0)
        stock_updated = models.DateTimeField(_("stock updated at"),
                default=timezone.now(), # default value for migration
                editable=False) 
	price = models.FloatField(_("retail price"), null=True, blank=True)
        price_updated = models.DateTimeField(_("price updated at"),
                default=timezone.now(), #default value for migration
                editable=False)
	stock_value = models.FloatField(_("stock value"), default=0)
        stock_value_updated = models.DateTimeField(_("stock value updated at"),
                default=timezone.now(), #default value for migration
                editable=False)
	documents = models.ManyToManyField(Document,
		blank=True,
		null=True,
		related_name="articles",
		verbose_name=_("documents")
	)

	class Meta:
		ordering = ['-favorited', '-enabled', 'code',]
		unique_together = [('code', 'brand'),]
		verbose_name = _("article")
		verbose_name_plural = _("articles")
	
	def __unicode__(self):
		return self.code

        def __init__(self, *args, **kwargs):
            super(Article, self).__init__(*args, **kwargs)
            self.__original_stock = self.stock
            self.__original_price = self.price
            self.__original_stock_value = self.stock_value

        def save(self, force_insert=False, force_update=False, *args, **kwargs):
            if self.stock != self.__original_stock:
                self.control_stock = True
                self.stock_updated = timezone.now()
            if self.price != self.__original_price:
                self.price_updated = timezone.now()
            if self.stock_value != self.__original_stock_value:
                self.stock_value_updated = timezone.now()
            if not self.enabled:
                self.favorited = False
            super(Article, self).save(force_insert, force_update,
                    *args, **kwargs)
            self.__original_stock = self.stock
            self.__original_price = self.price

	@models.permalink
	def get_absolute_url(self):
		return('wm_article_detail', [self.id])

        def update_stock(self, items=0):
            if not self.control_stock:
                return
            try:
                i = int(items)
            except ValueError:
                i = 0
            self.stock += i
            if self.stock < 0:
                self.stock = 0
            #self.stock_updated = timezone.now()
            self.save()

        @property
        def show_stock_warning(self):
            return (self.stock < self.stock_alert) or not self.control_stock

        def toggle_favorite(self):
            """Mark/unmark an article as favorited. A favorited article should
            be also enabled."""
            self.favorited = not self.favorited
            if self.favorited and not self.enabled:
                self.enabled = True
            self.save()

class SupplierCode(models.Model):
	article = models.ForeignKey(Article, verbose_name=_("article"))
	company = models.ForeignKey(Company, verbose_name=_("company"))
	code = models.CharField(_("code"), max_length=50)

	class Meta:
		unique_together = [('article', 'company'),]
		verbose_name = _("supplier code")
		verbose_name_plural = _("supplier codes")

	def __unicode__(self):
		return self.code

