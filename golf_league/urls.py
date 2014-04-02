from django.conf.urls import patterns, include, url
from golf_league import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
handler404 = 'golf.views.custom_404'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'golf_league.views.home', name='home'),
    # url(r'^golf_league/', include('golf_league.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^golf/', include('golf.urls')),
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )