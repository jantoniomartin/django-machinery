from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from om.models import *

class OrderItemInline(admin.TabularInline):
	model = OrderItem
	fields = (
		'article_code',
		'ordered_quantity',
		'received_quantity',
		'completed_on',
		'estimated_delivery',)
	
	readonly_fields = ('article_code',)

	def article_code(self, instance):
		return unicode(instance.offer.article)

	article_code.short_description = _("Article code")

class OrderAdmin(admin.ModelAdmin):
	inlines = [OrderItemInline,]

admin.site.register(Offer)
admin.site.register(Order, OrderAdmin)
admin.site.register(CartItem)
admin.site.register(CsvTemplate)
