import datetime

from django.views.generic.base import TemplateView
from django.conf import settings

import pm.models as pm

class DashboardView(TemplateView):
	template_name = "dashboard.html"

	def get_context_data(self, **kwargs):
		context = super(DashboardView, self).get_context_data(**kwargs)
		min_year = getattr(settings, "PM_RUNNING_ALL_BEFORE_YEAR", 1900)
		active_projects = pm.Project.objects.filter(
			machine__shipped_on__isnull=True,
			machine__running_on__isnull=True,
			machine__created_on__gt=datetime.date(min_year, 1, 1)
		).distinct()
		shipped_projects = pm.Project.objects.filter(
			machine__shipped_on__isnull=False,
			machine__running_on__isnull=True,
			machine__created_on__gt=datetime.date(min_year, 1, 1)
		).distinct()
		context.update({
			'active_projects': active_projects,
			'shipped_projects': shipped_projects,
		})
		return context

