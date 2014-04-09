from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from model_utils.managers import PassThroughManager

from crm.defaults import *
from crm import querysets

class Group(models.Model):
	"""
	Group represents a corporate group, that includes more than one company
	"""
	name = models.CharField(_("name"), max_length=50, unique=True)

	class Meta:
		ordering = ['name',]
		verbose_name = _("group")
		verbose_name_plural = _("groups")
		permissions = (('view_group', 'Can view group'),)

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
		permissions = (('view_company', 'Can view company'),)

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
		permissions = (('view_department', 'Can view department'),)

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('crm_department_detail', [self.id])

class SalesDocument(models.Model):
	company = models.ForeignKey(Company, verbose_name=_("company"))
	author = models.ForeignKey(User, verbose_name=_("author"))
	language = models.CharField(_("language"), max_length=8,
		choices=REPORT_LANGUAGES)
	disaggregated = models.BooleanField(_("disaggregated"), default=True)
	total = models.DecimalField(_("total"), max_digits=12, decimal_places=2,
		blank=True, null=True)

	class Meta:
		abstract = True
		ordering = ['-id',]

	def __unicode__(self):
		return u"%(year)s-%(company)s-%(id)s" % {
			"year": self.created.strftime("%y"),
			"company": self.company.id,
			"id": self.id
		}

class SalesDocumentItem(models.Model):
	quantity = models.PositiveIntegerField(_("quantity"), default=1)
	description = models.TextField(_("description"))
	price = models.DecimalField(_("price"), max_digits=12, decimal_places=2,
		blank=True, null=True)

	class Meta:
		abstract = True

	def __unicode__(self):
		return unicode(self.id)

class Quotation(SalesDocument):
	created = models.DateField(_("created"), auto_now_add=True)
	recipient_name = models.CharField(_("recipient name"), max_length=255,
		blank=True, null=True)
	title = models.CharField(_("title"), max_length=255)
	conditions = models.TextField(_("conditions"), blank=True, null=True)
	private_note = models.CharField(_("private note"), max_length=255,
		blank=True, null=True)

	class Meta(SalesDocument.Meta):
		verbose_name = _("quotation")
		verbose_name_plural = _("quotations")
		permissions = (('view_quotation', 'Can view quotation'),)

	@models.permalink
	def get_absolute_url(self):
		return ('crm_quotation_detail', [self.id])

class QuotationItem(SalesDocumentItem):
	quotation = models.ForeignKey(Quotation, verbose_name=_("quotation"))
	optional = models.BooleanField(_("optional"), default=False)

	objects = PassThroughManager.for_queryset_class(
		querysets.QuotationItemQuerySet)()

	class Meta(SalesDocumentItem.Meta):
		verbose_name = _("quotation item")
		verbose_name_plural = _("quotation items")
	
class Contract(SalesDocument):
	created = models.DateField(_("created"))
	delivery_time = models.TextField(_("delivery time"), default="", blank=True)
	delivery_method = models.CharField(_("delivery method"), max_length=255,
		default="", blank=True)
	conditions = models.TextField(_("conditions"), blank=True, default="")
	remarks = models.TextField(_("remarks"), default="", blank=True)
	vat = models.DecimalField(_("VAT"), max_digits=4, decimal_places=2,
		choices=VAT_CHOICES)
	signed_copy = models.FileField(_("signed copy"), upload_to="crm/contracts",
		blank=True, null=True)

	class Meta(SalesDocument.Meta):
		verbose_name = _("contract")
		verbose_name_plural = _("contracts")
		permissions = (('view_contract', 'Can view contract'),)

	def __unicode__(self):
		return "".join(["C",
			super(Contract, self).__unicode__()]
		)

	@models.permalink
	def get_absolute_url(self):
		return ('crm_contract_detail', [self.id])

class ContractItem(SalesDocumentItem):
	contract = models.ForeignKey(Contract, verbose_name=_("contract"))
	
	objects = PassThroughManager.for_queryset_class(
		querysets.ContractItemQuerySet)()

	class Meta(SalesDocumentItem.Meta):
		verbose_name = _("contract item")
		verbose_name_plural = _("contract items")
	
class Proforma(SalesDocument):
	created = models.DateField(_("created"))
	remarks = models.TextField(_("remarks"), default="", blank=True)
	vat = models.DecimalField(_("VAT"), max_digits=4, decimal_places=2,
		choices=VAT_CHOICES)

	class Meta(SalesDocument.Meta):
		verbose_name = _("proforma")
		verbose_name_plural = _("proformas")
		permissions = (('view_proforma', 'Can view proforma'),)

	def __unicode__(self):
		return "".join(["P",
			super(Proforma, self).__unicode__()]
		)

	@models.permalink
	def get_absolute_url(self):
		return ('crm_proforma_detail', [self.id])

class ProformaItem(SalesDocumentItem):
	proforma = models.ForeignKey(Proforma, verbose_name=_("proforma"))
	
	class Meta(SalesDocumentItem.Meta):
		verbose_name = _("proforma item")
		verbose_name_plural = _("proforma items")
	
class DeliveryNote(models.Model):
	contract = models.ForeignKey(Contract, verbose_name=_("contract"))
	created = models.DateField(_("created"), auto_now_add=True)
	remarks = models.TextField(_("remarks"), default="", blank=True)

	class Meta:
		ordering = ['-id',]
		verbose_name = _("delivery note")
		verbose_name_plural = _("delivery notes")
		permissions = (('view_deliverynote', 'Can view delivery note'),)

	def __unicode__(self):
		return u"A%(year)s-%(company)s-%(id)s" % {
			"year": self.created.strftime("%y"),
			"company": self.contract.company.id,
			"id": self.id
		}

	@models.permalink
	def get_absolute_url(self):
		return ('crm_deliverynote_detail', [self.id])

class DeliveryNoteItem(models.Model):
	note = models.ForeignKey(DeliveryNote, verbose_name=_("delivery note"))
	quantity = models.PositiveIntegerField(_("quantity"), default=1)
	description = models.TextField(_("description"))

	class Meta:
		verbose_name = _("delivery note item")
		verbose_name_plural = _("delivery note items")
	
	def __unicode__(self):
		return unicode(self.id)

