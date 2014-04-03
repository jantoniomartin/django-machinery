from django.contrib import admin

from crm.models import *

admin.site.register(Group)
admin.site.register(Company)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Department)
admin.site.register(Quotation)
admin.site.register(QuotationItem)
