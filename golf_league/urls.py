from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'golf_league.views.home', name='home'),
    # url(r'^golf_league/', include('golf_league.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Add this to get widgets.AdminDateWidget() working
    url(r'^admin/jsi18n/$', 'django.views.i18n.__javascript__catalog'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^golf/', include('golf.urls')),
)
