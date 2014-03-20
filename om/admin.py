from django.contrib import admin

from om.models import *

admin.site.register(Offer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(CsvTemplate)
