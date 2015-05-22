from django.conf.urls import patterns, url

from profiles.views import *

urlpatterns = patterns("profiles.views",
    url(r'^employees/barcodes$',
        EmployeeCodesView.as_view(),
        name="profiles_employee_codes"
    ),
)
