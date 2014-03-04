from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from wm import models

def import_all():
	msg = import_brands()
	msg += import_groups()
	msg += import_articles()
	return msg

def setup_cursor():
	if settings.MIGRATION_DB is None:
		return None
	from django.db import connections
	cursor = connections[settings.MIGRATION_DB].cursor()
	return cursor

def import_brands():
	cursor = setup_cursor()
	if cursor is None:
		return
	sql = """SELECT DISTINCT trademark FROM articles
			WHERE trademark != ''"""
	cursor.execute(sql)
	msg = u"Error report for Brands:\n"
	n = 0
	for row in cursor.fetchall():
		brand = models.Brand(name=row[0])
		try:
			brand.save()
		except:
			msg += u"Couldn't import Brand %s\n" % row[0]
		else:
			n += 1
	print u"Created %s brands" % n
	return msg

def import_groups():
	cursor = setup_cursor()
	if cursor is None:
		return
	n = 0
	c = 1
	ids = ["0",]
	msg = u"Error report for Groups:\n"
	while c > 0:
		c = 0
		idstring = ", ".join(ids)
		sql = """SELECT id, parent_id, name FROM boxes
				WHERE parent_id in (%s)""" % idstring
		cursor.execute(sql)
		ids = []
		for row in cursor.fetchall():
			if row[1] == 0:
				## root nodes
				#node = models.Group.add_root(id=row[0], name=row[2])
				node = models.Group.objects.create(id=row[0], name=row[2])
				ids.append(str(node.id))
				c += 1
				n += 1
			else:
				## child nodes
				try:
					parent = models.Group.objects.get(id=row[1])
				except ObjectDoesNotExist:
					msg += u"Error: parent with id %s not found" % row[1]
					return
				else:
					#node = parent.add_child(id=row[0], name=row[2])
					node = models.Group.objects.create(id=row[0], name=row[2],
						parent=parent)
					ids.append(str(node.id))
					c += 1
					n += 1
	print u"Imported %s groups" % n
	return msg

def import_articles():
	cursor = setup_cursor()
	if cursor is None:
		return
	sql = """SELECT id, code, description, trademark, measure_unit,
			standard_packing, box_id, enabled FROM articles
			"""
	cursor.execute(sql)
	msg = u"Error report for Articles:\n"
	n = 0
	for row in cursor.fetchall():
		try:
			brand = models.Brand.objects.get(name=row[3])
		except ObjectDoesNotExist:
			brand = None
		try:
			group = models.Group.objects.get(id=row[6])
		except:
			msg += u"Group with id %s not found\n" % row[6]
			continue
		else:
			article = models.Article(id=row[0], code=row[1], description=row[2],
				measure_unit=row[4], enabled=row[7],
				brand=brand, group=group)
			if not row[5] is None:
				article.packaging = row[5]
			try:
				article.save()
			except:
				msg += u"Article with id %s could not be saved\n" % row[0]
			else:
				n += 1
	print u"Imported %s articles" % n
	return msg
