from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from indumatic.views import DashboardView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', DashboardView.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')i),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^search/', include('haystack.urls')),
	url(r'^crm/', include('crm.urls')),
	url(r'^om/', include('om.urls')),
	url(r'^pm/', include('pm.urls')),
	url(r'^wm/', include('wm.urls')),
)
