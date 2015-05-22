import os

#import ho.pisa as pisa
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import cgi

from django.conf import settings

def fetch_resources(uri, rel):
	sUrl = settings.STATIC_URL
	sDirs = settings.STATICFILES_DIRS
	mUrl = settings.MEDIA_URL
	mRoot = settings.MEDIA_ROOT
	if uri.startswith(mUrl):
		path = os.path.join(mRoot, uri.replace(mUrl, ""))
	elif uri.startswith(sUrl):
		path = os.path.join(sDirs[0], uri.replace(sUrl, ""))

	if not os.path.isfile(path):
		raise Exception(
			'media URI must start with %s or %s' % (sUrl, mUrl)
		)
	return path


def make_pdf(html):
	""" Make the pdf file and return it as HttpResponse """
	result = StringIO.StringIO()
	pdf = pisa.pisaDocument(
		StringIO.StringIO(html.encode("UTF-8")),
		dest=result,
		link_callback=fetch_resources
	)
	if not pdf.err:
		return result
	else:
		raise Exception('Error al generar el PDF: %s' % cgi.escape(html))

