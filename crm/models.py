#from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class Group(models.Model):
	"""
	Group represents a corporate group, that includes more than one company
	"""
	name = models.CharField(_("name"), max_length=50, unique=True)

	class Meta:
		ordering = ['name',]
		verbose_name = _("group")
		verbose_name_plural = _("groups")

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('crm_group_detail', [self.id])

class Company(models.Model):
	name = models.CharField(_("name"), max_length=255, unique=True)
	vatin = models.CharField(_("VATIN"), max_length=16, blank=True, null=True)
	address = models.CharField(_("address"), max_length=255, blank=True,
		null=True)
	city = models.CharField(_("city"), max_length=50, blank=True, null=True)
	region = models.CharField(_("region"), max_length=50, blank=True, null=True)
	postal_code = models.CharField(_("postal code"), max_length=10, blank=True,
		null=True)
	country = models.CharField(_("country"), max_length=50, blank=True,
		null=True)
	comment = models.TextField(_("comment"), blank=True, null=True)
	website = models.URLField(_("website"), max_length=200,
		blank=True, null=True)
	global_email = models.EmailField(_("global email"), max_length=75, blank=True, null=True)
	main_phone = models.CharField(_("main phone"), max_length=40, blank=True, null=True)
	secondary_phone = models.CharField(_("secondary_phone"), max_length=40, blank=True, null=True)
	fax = models.CharField(_("fax"), max_length=40, blank=True, null=True)
	created_at = models.DateTimeField(_("created at"), auto_now_add=True)
	updated_at = models.DateTimeField(_("updated at"), auto_now=True)
	is_customer = models.BooleanField(_(" is customer"), default=False)
	is_supplier = models.BooleanField(_(" is supplier"), default=False)
	group = models.ForeignKey(Group, verbose_name=_("group"), null=True,
		blank=True)

	class Meta:
		ordering = ['name', ]
		verbose_name = _("company")
		verbose_name_plural = _("companies")

	def __unicode__(self):
		return self.name
	
	@models.permalink
	def get_absolute_url(self):
		return ('crm_company_detail', [self.id])

	@property
	def order_emails_list(self):
		return self.department_set.filter(
			email__isnull=False,
			send_orders=True
		).values_list('email', flat=True)

class Customer(Company):
	pass

	class Meta:
		proxy = True
		verbose_name = _("customer")
		verbose_name_plural = _("customers")

class Supplier(Company):
	pass

	class Meta:
		proxy = True
		verbose_name = _("supplier")
		verbose_name_plural = _("suppliers")

class Department(models.Model):
	name = models.CharField(_("name"), max_length=50)
	person = models.CharField(_("person"), max_length=100, blank=True,
		null=True)
	phone = models.CharField(_("phone"), max_length=40, blank=True, null=True)
	email = models.EmailField(_("email"), max_length=75, blank=True, null=True)
	send_orders = models.BooleanField(_("send orders"), default=False)
	comment = models.CharField(_("comment"), max_length=255, blank=True,
		null=True)
	company = models.ForeignKey(Company, null=True, blank=True,
		verbose_name=_("company"))

	class Meta:
		ordering = ['name', ]
		verbose_name = _("department")
		verbose_name_plural = _("departments")

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('crm_department_detail', [self.id])

