from django.conf.urls import patterns, url
from mappingapp import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^results/', views.results, name='results'),
        url(r'^search/', views.search, name='search'))


