from django.conf.urls import patterns, url
from mappingapp import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^results/', views.results, name='results'),
        url(r'^search/', views.search, name='search'),
        url(r'^upload/', views.upload, name='upload'),
        url(r'^edit/', views.edit, name='edit'),
        url(r'^edittcn/', views.edittcn, name='edittcn'),
        url(r'^login/$', views.userlogin, name='userlogin'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^sites/$', views.sites, name='sites'),
        )


