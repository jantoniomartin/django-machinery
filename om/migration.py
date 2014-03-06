from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from om import models
from wm.models import Article
from crm.models import Company

def import_all():
	msg = import_offers()
	msg += import_orders()
	msg += import_orderitems()
	return msg

def setup_cursor():
	if settings.MIGRATION_DB is None:
		return None
	from django.db import connections
	cursor = connections[settings.MIGRATION_DB].cursor()
	return cursor

def import_offers():
	cursor = setup_cursor()
	if cursor is None:
		return
	sql = """SELECT id, article_id, organization_id, offered_on, confirmed_on,
		expires_on, code, trade_price, price
		FROM offers"""
	cursor.execute(sql)
	n = 0
	msg = u""
	for row in cursor.fetchall():
		try:
			article = Article.objects.get(id=row[1])
		except ObjectDoesNotExist:
			msg += u"Article does not exist for offer id %s\n" % row[0]
			continue
		try:
			company = Company.objects.get(id=row[2])
		except ObjectDoesNotExist:
			msg += u"Company does not exist for offer id %s\n" % row[0]
			continue
		offer = models.Offer(id=row[0], article=article, company=company,
			confirmed_on=row[4], expired_on=row[5], code=row[6],
			retail_price=row[8], invoice_price=row[7])
		offer.save()
		if not (row[3] is None or row[3] == ''):
			offer.offered_on = row[3]
		else:
			if not (row[4] is None or row[4] == ''):
				offer.offered_on = row[4]
			elif not (row[5] is None or row[5] == ''):
				offer.offered_on = row[5]
			else:
				offer.offered_on = '1998-01-01'
		offer.save()
		n += 1
	print "Imported %s offers" % n
	return msg

def import_orders():
	cursor = setup_cursor()
	if cursor is None:
		return
	sql = """SELECT id, reference, created_at, notes, means, organization_id
		FROM orders"""
	cursor.execute(sql)
	n = 0
	msg = u""
	for row in cursor.fetchall():
		try:
			company = Company.objects.get(id=row[5])
		except ObjectDoesNotExist:
			msg += u"Company does not exist for order id %s\n" % row[0]
			continue
		reference = int(row[1][2:])
		order = models.Order(id=row[0], reference=reference, notes=row[3],
			company=company)
		order.save()
		order.created_at = row[2]
		order.save()
		n += 1
	print "Imported %s orders" % n
	return msg

def import_orderitems():
	cursor = setup_cursor()
	if cursor is None:
		return
	sql = """SELECT id, ordered_quantity, received_quantity, completed_on,
		estimated_delivery_on, order_id, offer_id
		FROM order_lines"""
	cursor.execute(sql)
	n = 0
	msg = u""
	for row in cursor.fetchall():
		try:
			order = models.Order.objects.get(id=row[5])
		except ObjectDoesNotExist:
			msg += u"Order not found for order line %s\n" % row[0]
			continue
		try:
			offer = models.Offer.objects.get(id=row[6])
		except ObjectDoesNotExist:
			msg += u"Offer not found for order line %s" % row[0]
			continue
		orderitem = models.OrderItem(ordered_quantity=row[1],
			received_quantity=row[2], completed_on=row[3],
			estimated_delivery=row[4], order=order, offer=offer)
		orderitem.save()
		n += 1
	print "Imported %s order items" % n
	return msg
