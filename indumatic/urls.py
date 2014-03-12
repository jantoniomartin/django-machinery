from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout_then_login

from django.contrib import admin
admin.autodiscover()

from indumatic.views import DashboardView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', DashboardView.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')i),
	url(r'^auth/logout/$',
		logout_then_login,
		{'login_url': '/auth/login/'},
		name='logout_then_login'),
	url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^search/', include('haystack.urls')),
	url(r'^crm/', include('crm.urls')),
	url(r'^om/', include('om.urls')),
	url(r'^pm/', include('pm.urls')),
	url(r'^wm/', include('wm.urls')),
)
