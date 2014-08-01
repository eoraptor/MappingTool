from django.conf.urls import patterns, url
from mappingapp import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^search/', views.search, name='search'),
                       url(r'^upload/', views.upload, name='upload'),
                       url(r'^edit/', views.edit, name='edit'),
                       url(r'^validatesample/', views.validatesample, name='validatesample'),
                       url(r'^login/$', views.userlogin, name='userlogin'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^sites/$', views.sites, name='sites'),
                       url(r'^markers/$', views.markers, name='markers'),
                       url(r'^create_site/$', views.create_site, name='create_site'),
                       url(r'^check_sample/$', views.check_sample, name='check_sample'),
                       url(r'^editsample/$', views.editsample, name='editsample'),
                       url(r'^filesummary/$', views.filesummary, name='filesummary'),
                       url(r'^incrementcounter/$', views.incrementcounter, name='incrementcounter'),
                       url(r'^query/$', views.query, name='query'),
                       )


