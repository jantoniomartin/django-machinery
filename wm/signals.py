from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from wm.models import Group
from om.models import Offer

@receiver(post_save, sender=Group)
def clear_tree_cache(sender, instance, created, raw, using, **kwargs):
	key = make_template_fragment_key('groups_tree', [])
	if cache.get(key):
		cache.delete(key)

@receiver(post_save, sender=Offer)
def update_price_from_offer(sender, instance, created, raw, using, **kwargs):
    if instance.invoice_price is not None:
        if instance.article.stock_value is None or \
            timezone.now() >= instance.article.stock_value_updated:
            instance.article.stock_value = instance.invoice_price
            instance.article.save()

