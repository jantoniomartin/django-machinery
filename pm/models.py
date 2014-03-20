import os

from PIL import Image
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from crm.models import Company
from wm.models import Article

class Sector(models.Model):
	code = models.CharField(_("code"), max_length=3, unique=True)
	description = models.CharField(_("description"), max_length=50)

	class Meta:
		verbose_name = _("sector")
		verbose_name_plural = _("sectors")

	def __unicode__(self):
		return self.description

	@models.permalink
	def get_absolute_url(self):
		return ('pm_sector_detail', [self.id])

def project_thumbnail(instance, filename):
	return os.path.join("thumbnails", "%s.jpg" % instance.serial)

class Project(models.Model):
	sector = models.ForeignKey(Sector, verbose_name=_("sector"))
	serial = models.CharField(_("serial number"), max_length=4)
	old_model = models.CharField(_("old model"), max_length=5,
		blank=True, null=True)
	description = models.CharField(_("description"), max_length=255)
	notes = models.TextField(_("notes"), blank=True, null=True)
	is_retired = models.BooleanField(_("retired"), default=False)
	created_on = models.DateField(_("created on"), auto_now_add=True, null=True)
	company = models.ForeignKey(Company, verbose_name=_("company"))
	thumbnail = models.ImageField(_("thumbnail"), upload_to=project_thumbnail, null=True, blank=True)

	class Meta:
		verbose_name = _("project")
		verbose_name_plural = _("projects")
		ordering = ["-serial",]

	def __unicode__(self):
		if self.old_model:
			return u"%(model)s-%(serial)s" % {'model': self.old_model,
											'serial': self.serial,}
		return u"%(sector)s-%(serial)s" % {'sector': self.sector.code,
											'serial': self.serial,}

	@models.permalink
	def get_absolute_url(self):
		return ('pm_project_detail', [self.id])

	def save(self, force_insert=False, force_update=False):
		super(Project, self).save(force_insert, force_update)
		if self.thumbnail:
			pw = self.thumbnail.width
			ph = self.thumbnail.height
			## max height = 240px
			if ph > 240:
				height = 240
				width = int(pw * 240.0 / ph)
				filename = str(self.thumbnail.path)
				im = Image.open(filename)
				im = im.resize((width, height), Image.ANTIALIAS)
				im.save(self.thumbnail.path)

class Machine(models.Model):
	model = models.CharField(_("model"), max_length=3)
	number = models.CharField(_("number"), max_length=2)
	description = models.CharField(_("description"), max_length=255)
	created_on = models.DateField(_("created on"), auto_now_add=True, null=True)
	shipped_on = models.DateField(_("shipped on"), null=True, blank=True)
	running_on = models.DateField(_("running on"), null=True, blank=True)
	estimated_delivery_on = models.DateField(_("estimated delivery"), null=True, blank=True)
	is_retired = models.BooleanField(_("retired"), default=False)
	project = models.ForeignKey(Project, verbose_name=_("project"))

	class Meta:
		ordering = ['number',]
		unique_together = [('number', 'project'),]
		verbose_name = _("machine")
		verbose_name_plural = _("machines")

	def __unicode__(self):
		return u"%(model)s%(number)s" % {'model': self.model,
										'number': self.number }
	
	@property
	def full_reference(self):
		return u"%s-%s" % (self.project, self)

	@models.permalink
	def get_absolute_url(self):
		return ('pm_machine_detail', [self.id])

class MachineComment(models.Model):
	machine = models.ForeignKey(Machine, verbose_name=_("machine"))
	body = models.TextField(_("body"))
	created_on = models.DateField(_("created on"), auto_now_add=True)

	class Meta:
		verbose_name = _("machine comment")
		verbose_name_plural = _("machine comments")

	def __unicode__(self):
		return self.body

class Part(models.Model):
    article = models.ForeignKey(Article, verbose_name=_("article"))
    machine = models.ForeignKey(Machine, verbose_name=_("machine"))
    quantity = models.FloatField(_("quantity"))
    function = models.CharField(_("function"), max_length=255)

    class Meta:
        ordering = ["pk",]
        verbose_name = _("part")
        verbose_name_plural = _("parts")

    def __unicode__(self):
		return unicode(self.article)

@receiver(post_save, sender=Part)
def decrease_stock(sender, instance, created, raw, using, **kwargs):
	if created:
		if instance.article.control_stock:
			instance.article.stock -= instance.quantity
			if instance.article.stock < 0:
				instance.article.stock = 0
			instance.article.save()
