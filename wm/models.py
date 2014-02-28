from django.db import models
from django.utils.translation import ugettext_lazy as _

from treebeard import ns_tree

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

class Group(ns_tree.NS_Node):
	name = models.CharField(_("name"), max_length=50)

	class Meta:
		ordering = ['tree_id', 'lft']
		verbose_name = _("group")
		verbose_name_plural = _("groups")

	def __unicode__(self):
		return self.name
	
	@models.permalink
	def get_absolute_url(self):
		return('wm_group_detail', [self.id])

	@property
	def path(self):
		path = list(self.get_ancestors())
		path.append(self)
		return path

	@property
	def children(self):
		return self.get_children()

class Article(models.Model):
	code = models.CharField(_("code"), max_length=128)
	description = models.CharField(_("description"), max_length=255)
	measure_unit = models.CharField(_("measure unit"), max_length=10,
		blank=True, null=True)
	packaging = models.PositiveIntegerField(_("standard packaging"), default=1)
	enabled = models.BooleanField(_("enabled"), default=True)
	brand = models.ForeignKey(Brand, verbose_name=_("brand"), null=True, blank=True)
	group = models.ForeignKey(Group, verbose_name=_("group"))

	class Meta:
		ordering = ['-id',]
		unique_together = [('code', 'brand'),]
		verbose_name = _("article")
		verbose_name_plural = _("articles")
	
	def __unicode__(self):
		return self.code

	@models.permalink
	def get_absolute_url(self):
		return('wm_article_detail', [self.id])

