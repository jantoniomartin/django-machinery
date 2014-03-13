import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from pm import models
import crm.models as crm
import wm.models as wm

def import_all():
	msg = import_sectors()
	msg += import_projects()
	msg += import_thumbs()
	msg += import_machines()
	msg += import_comments()
	return msg

def setup_cursor():
	if settings.MIGRATION_DB is None:
		return None
	from django.db import connections
	cursor = connections[settings.MIGRATION_DB].cursor()
	return cursor

def import_sectors():
	cursor = setup_cursor()
	if cursor is None:
		return
	sql = """SELECT DISTINCT sector FROM projects"""
	cursor.execute(sql)
	msg = u"Error report for Sectos:\n"
	n = 0
	for row in cursor.fetchall():
		sector = models.Sector(code=row[0],
							description="Temporary description")
		try:
			sector.save()
		except:
			msg += u"Couldn't import Sector %s\n" % row[0]
		else:
			n += 1
	print "Created %s sectors" % n
	return msg

def import_thumbs():
	cursor = setup_cursor()
	if cursor is None:
		return
	sql = """SELECT id, serial, thumbnail FROM projects"""
	cursor.execute(sql)
	msg = u"Error report for Thumbnails:\n"
	n = 0
	for row in cursor.fetchall():
		try:
			project = models.Project.objects.get(id=row[0])
		except ObjectDoesNotExist:
			msg += u"Project not found: %s" % row[0]
		else:
			if row[1] is not None:
				fname = os.path.join("thumbnails", "%s.jpg" % row[1])
				path = os.path.join(
					settings.MEDIA_ROOT, 
					fname
				)
				f = open(path, 'w')
				f.write(row[2])
				try:
					project.thumbnail = fname
					project.save()
					f.close()
				except:
					msg += u"Thumbnail not saved: %s" % row[0]
				else:
					n +=1
	print "Imported %s thumbnails" % n
	return msg

def import_projects():
	cursor = setup_cursor()
	if cursor is None:
		return
	sql = """SELECT id, sector, serial, old_model, description, notes,
			is_retired, created_on, organization_id
			FROM projects"""
	cursor.execute(sql)
	msg = u"Error report for Projects:\n"
	n = 0
	for row in cursor.fetchall():
		try:
			company = crm.Company.objects.get(id=row[8])
		except ObjectDoesNotExist:
			msg += u"Company not found for project %s" % row[8]
		else:
			try:
				sector = models.Sector.objects.get(code=row[1])
			except ObjectDoesNotExist:
				msg += u"Sector not found for project %s" % row[0]
			else:
				project = models.Project(id=row[0],
										sector=sector,
										serial=row[2],
										old_model=row[3],
										description=row[4],
										notes=row[5],
										is_retired=row[6],
										company=company)
				try:
					project.save()
					project.created_on = row[7]
					project.save()
				except:
					msg += u"Couldn't import project with id=%s\n" % row[0]
				else:
					n += 1
	print u"Imported %s projects" % n
	return msg

def import_machines():
	cursor = setup_cursor()
	if cursor is None:
		return
	sql = """SELECT id, model, number, description, created_on,
			shipped_on, running_on, estimated_delivery_on, is_retired,
			project_id
			FROM machines"""
	cursor.execute(sql)
	msg = u"Error report for Machines:\n"
	n = 0
	for row in cursor.fetchall():
		try:
			project = models.Project.objects.get(id=row[9])
		except ObjectDoesNotExist:
			msg += u"Project not found for machine %s" % row[0]
		else:
			machine = models.Machine(id=row[0],
									model=row[1],
									number=row[2],
									description=row[3],
									shipped_on=row[5],
									running_on=row[6],
									estimated_delivery_on=row[7],
									is_retired=row[8],
									project=project)
			try:
				machine.save()
				machine.created_on = row[4]
				machine.save()
			except:
				msg += u"Couldn't import Machine with id=%s\n" % row[0]
			else:
				n += 1
	print u"Imported %s machines" % n
	return msg

def import_comments():
	cursor = setup_cursor()
	if cursor is None:
		return
	sql = """SELECT body, created_on, machine_id
			FROM comments WHERE machine_id is not null"""
	cursor.execute(sql)
	n = 0
	msg = u"Error report for Comments:\n"
	for row in cursor.fetchall():
		try:
			machine = models.Machine.objects.get(id=row[2])
		except ObjectDoesNotExist:
			msg += u"Machine not found with id %s" % row[2]
		else:
			comment = models.MachineComment(machine=machine,
											body=row[0])
			try:
				comment.save()
				comment.created_on = row[1]
				comment.save()
			except:
				msg += u"Couldn't import Comment with machine_id=%s\n" % row[2]
			else:
				n += 1
	print u"Imported %s comments" % n
	return msg

def import_parts():
	cursor = setup_cursor()
	if cursor is None:
		return
	sql = """SELECT id, article_id, machine_id, quantity, job
		FROM parts"""
	cursor.execute(sql)
	n = 0
	msg = u"Error report for Parts:\n"
	for row in cursor.fetchall():
		try:
			article = wm.Article.objects.get(id=row[1])
		except ObjectDoesNotExist:
			msg += u"Article not found for part %s" % row[0]
			continue
		try:
			machine = models.Machine.objects.get(id=row[2])
		except ObjectDoesNotExist:
			msg += u"Machine not found for part %s" % row[0]
			continue
		function = row[4]
		if function is None:
			function = u"No definido"
		part = models.Part(article=article, machine=machine,
			quantity=row[3], function=function)
		try:
			part.save()
		except Exception, e:
			print e
			msg += u"Couldn't save part %s\n" % row[0]
		else:
			n += 1
	print "Imported %s parts" % n
	return msg
