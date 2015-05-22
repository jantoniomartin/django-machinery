import unicodedata

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Employee(models.Model):
    user = models.OneToOneField(User)
    department = models.CharField(_("department"), max_length=100)
    mobile = models.CharField(_("mobile phone"), max_length=40, blank=True,
            null=True)

    class Meta:
        verbose_name = _("employee")
        verbose_name_plural = _("employees")

    def __unicode__(self):
        return unicode(self.user)

    def codename(self):
        """Return a unique string to be used in a barcode (Code39)"""
        name = "%s %s %s" % (self.user.id, self.user.last_name,
            self.user.first_name)
        name = name[0:39]
        return unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')

