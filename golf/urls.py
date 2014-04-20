from django.conf.urls import patterns, url
from golf import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^golfer/(?P<golfer_id>\d+)/$', views.golfer, name='golfer'),
                       url(r'^course/(?P<course_id>\d+)/$', views.course, name='course'),
                       url(r'^round/(?P<round_id>\d+)/$', views.round, name='round'),
                       url(r'^courses/$', views.courses, name='courses'),
                       url(r'^rounds/(?P<week_num>\d+)/$', views.rounds, name='rounds'),
                       url(r'^roster/$', views.roster, name='roster'),
                       url(r'^add_golfer/$', views.add_golfer, name='add_golfer'),
                       url(r'^add_round/$', views.add_round, name='add_round'),
                       url(r'^add_course/$', views.add_course, name='add_course'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^about/$', views.about, name='about'),
                       url(r'^skins/$', views.skins, name='skins'),
                       )