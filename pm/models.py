import os

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import PassThroughManager

from pm import querysets
from crm.models import Company, ContractItem
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
	contract_item = models.ForeignKey(ContractItem,
		verbose_name=_("contract item"), blank=True, null=True)

	objects = PassThroughManager.for_queryset_class(querysets.MachineQuerySet)()
	
	class Meta:
		ordering = ['number',]
		unique_together = [('number', 'project'),]
		verbose_name = _("machine")
		verbose_name_plural = _("machines")

	def __unicode__(self):
		return u"%(model)s%(number)s" % {'model': self.model,
										'number': self.number }

	def save(self, *args, **kwargs):
		if not self.pk and not self.number:
			try:
				n = int(Machine.objects.filter(
					project=self.project).order_by("-number")[0].number)
			except IndexError:
				n = 0
			self.number = str(n + 1).zfill(2)
		return super(Machine, self).save(*args, **kwargs)

	@property
	def full_reference(self):
		return u"%s-%s" % (self.project, self)

	@models.permalink
	def get_absolute_url(self):
		return ('pm_machine_detail', [self.id])

	@property
	def contract_url(self):
		if self.contract_item:
			print self.contract_item.contract.get_absolute_url()
			return self.contract_item.contract.get_absolute_url()
		return None

class MachineComment(models.Model):
	machine = models.ForeignKey(Machine, verbose_name=_("machine"))
	body = models.TextField(_("body"))
	created_on = models.DateField(_("created on"), auto_now_add=True)
	author = models.ForeignKey(User, verbose_name=_("author"))

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

	objects = PassThroughManager.for_queryset_class(querysets.PartQuerySet)()

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

class CECertificate(models.Model):
	project = models.ForeignKey(Project, verbose_name=_("project"))
	date = models.DateField(_("date"))

	class Meta:
		verbose_name = _("CE certificate")
		verbose_name_plural = _("CE certificates")

	def __unicode__(self):
		return unicode(self.project)

TICKET_STATUS = (
	(0, _("The customer is waiting for an answer")),
	(1, _("Waiting for an answer from the customer")),
	(2, _("Closed")),
)

class Ticket(models.Model):
	project = models.ForeignKey(Project, verbose_name=_("project"))
	created_on = models.DateTimeField(_("created on"), auto_now_add=True)
	updated_on = models.DateTimeField(_("updated on"), auto_now=True)
	updated_by = models.ForeignKey(User, verbose_name=_("updated by"))
	status = models.PositiveIntegerField(_("status"), default=0,
		choices=TICKET_STATUS)
	summary = models.CharField(_("summary"), max_length=255)
	content = models.TextField(_("content"))

	class Meta:
		verbose_name = _("ticket")
		verbose_name_plural = _("tickets")
		ordering = ['-updated_on',]

	def __unicode__(self):
		return self.summary

	@models.permalink
	def get_absolute_url(self):
		return ('pm_ticket_detail', [self.id])

class TicketItem(models.Model):
	ticket = models.ForeignKey(Ticket, verbose_name=_("ticket"))
	created_on = models.DateTimeField(_("created on"), auto_now_add=True)
	created_by = models.ForeignKey(User, verbose_name=_("created_by"))
	content = models.TextField(_("content"))

	class Meta:
		verbose_name = _("ticket item")
		verbose_name_plural = _("ticket items")
	
	def __unicode__(self):
		return u"%s" % self.pk

