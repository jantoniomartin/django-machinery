from django.db import models
from django.utils.translation import ugettext_lazy as _

from uuidfield import UUIDField

class Document(models.Model):
	uuid = UUIDField(auto=True)
	document = models.FileField(_("document"), upload_to="dm")
	title = models.CharField(_("title"), max_length=255)
	description = models.CharField(_("description"), max_length=255,
		blank=True, null=True)
	created_at = models.DateTimeField(_("created at"), auto_now_add=True)

	class Meta:
		ordering = ['title',]
		verbose_name = _("document")
		verbose_name_plural = _("documents")

	def __unicode__(self):
		return self.title
