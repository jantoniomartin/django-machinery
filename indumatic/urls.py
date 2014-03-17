from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout_then_login

from django.contrib import admin
admin.autodiscover()

from indumatic.views import DashboardView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', DashboardView.as_view(), name='home'),
	#url(r'session_security/', include('session_security.urls')),
	url(r'^login/$', login, name="login"),
	url(r'^logout/$',
		logout_then_login,
		{'login_url': '/auth/login/'},
		name='logout_then_login'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^crm/', include('crm.urls')),
	url(r'^om/', include('om.urls')),
	url(r'^pm/', include('pm.urls')),
	url(r'^wm/', include('wm.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
