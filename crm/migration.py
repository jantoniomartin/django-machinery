from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from crm import models

def import_all():
	msg = import_companies()
	msg += import_departments()
	msg += import_sales_deps()
	return msg

def import_companies():
	if settings.MIGRATION_DB is None:
		return
	from django.db import connections
	cursor = connections[settings.MIGRATION_DB].cursor()
	sql = """SELECT id, name, cif, address, city, region, zip, country,
			notes, website, main_email, phone_1, phone_2, fax, is_customer,
			is_supplier, created_at
			FROM organizations"""
	cursor.execute(sql)
	msg = u"Error report for Companies:\n"
	n = 0
	for row in cursor.fetchall():
		company = models.Company(id=row[0],
						name=row[1],
						vatin=row[2],
						address=row[3],
						city=row[4],
						region=row[5],
						postal_code=row[6],
						country=row[7],
						comment=row[8],
						website=row[9],
						global_email=row[10],
						main_phone=row[11],
						secondary_phone=row[12],
						fax=row[13],
						is_customer=row[14],
						is_supplier=row[15])
		try:
			company.save()
			company.created_at = row[16]
			company.save()
		except:
			msg += u"Couldn't import Company for organization.id=%s\n" % row[0] 
		else:
			n += 1
	print u"Imported %s companies" % n
	return msg

def import_departments():
	if settings.MIGRATION_DB is None:
		return
	from django.db import connections
	cursor = connections[settings.MIGRATION_DB].cursor()
	sql = """SELECT id, name, surname, nickname, job, phone, email, notes,
			organization_id
			FROM people """
	cursor.execute(sql)
	msg = u"Error report for Person:\n"
	n = 0
	for row in cursor.fetchall():
		try:
			company = models.Company.objects.get(id=row[8])
		except ObjectDoesNotExist:
			msg += u"Company not found for person id %s\n" % row[0]
		else:
			if row[4] is None or row[4]=="":
				name = "Desconocido"
			else:
				name = row[4]
			department = models.Department(
								name=name,
								person=" ".join([row[1], row[2]]),
								phone=row[5],
								email=row[6],
								comment=row[7],
								company=company)
			try:
				department.save()
			except:
				msg += u"Couldn't import person with people.id=%s\n" % row[0]
			else:
				n += 1
	print u"Imported %s people" % n
	return msg

def import_sales_deps():
	if settings.MIGRATION_DB is None:
		return
	from django.db import connections
	cursor = connections[settings.MIGRATION_DB].cursor()
	sql = """SELECT id, orders_email
		FROM organizations
		WHERE orders_email IS NOT NULL"""
	cursor.execute(sql)
	msg = u"Error report for Sales Departments:\n"
	n = 0
	for row in cursor.fetchall():
		try:
			company = models.Company.objects.get(id=row[0])
		except ObjectDoesNotExist:
			msg += u"Company not found with organization.id=%s\n" % row[0]
		else:
			addresses = row[1].replace(" ", "").split(",")
			for address in addresses:
				department = models.Department(
					name = "Ventas",
					email=address,
					send_orders=True,
					company=company
				)
				try:
					department.save()
				except:
					msg += u"Couldn't import sales email with organization.id=%s\n" % row[0]
				else:
					n += 1
	print u"Imported %s sales emails" % n
	return msg

