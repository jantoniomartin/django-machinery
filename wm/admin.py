from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from wm.models import *

admin.site.register(Brand)
admin.site.register(Group, MPTTModelAdmin)
admin.site.register(Article)
admin.site.register(SupplierCode)
