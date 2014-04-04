from decimal import Decimal

from django.conf import settings

REPORT_LANGUAGES = getattr(settings,'CRM_REPORT_LANGUAGES',(('en', 'English'),))

COMPANY_CITY = getattr(settings, 'CRM_COMPANY_CITY', '')

COMPANY_ADDRESS = getattr(settings, 'CRM_COMPANY_ADDRESS', '')

VAT_CHOICES = getattr(settings, 'CRM_VAT_CHOICES', (
	(Decimal("0.00"), "0%"),
	(Decimal("21.00"), "21%"),
	))
