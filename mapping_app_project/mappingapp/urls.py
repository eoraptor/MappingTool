from django.conf.urls import patterns, url
from mappingapp import view_home, view_markers, view_contact, view_about, view_check_code, view_query\
    , view_create_site, view_get_site, view_suggest_code, view_error, view_search, view_upload, view_edit_select\
    , view_file_summary, view_validate_sample, view_increment_counter, view_edit_sample, view_login, view_logout\
    , view_create_new, view_upload_photograph, view_check_photofile, view_sample_photos, view_manage_photos\
    , view_photo_select


urlpatterns = patterns('',
                       url(r'^$', view_home.index, name='index'),
                       url(r'^search/', view_search.search, name='search'),
                       url(r'^upload/', view_upload.upload, name='upload'),
                       url(r'^edit/', view_edit_select.edit, name='edit'),
                       url(r'^validatesample/', view_validate_sample.validatesample, name='validatesample'),
                       url(r'^login/$', view_login.userlogin, name='userlogin'),
                       url(r'^logout/$', view_logout.user_logout, name='logout'),
                       url(r'^sites/$', view_get_site.sites, name='sites'),
                       url(r'^markers/$', view_markers.markers, name='markers'),
                       url(r'^create_site/$', view_create_site.create_site, name='create_site'),
                       url(r'^check_sample/$', view_check_code.check_sample, name='check_sample'),
                       url(r'^editsample/$', view_edit_sample.editsample, name='editsample'),
                       url(r'^filesummary/$', view_file_summary.filesummary, name='filesummary'),
                       url(r'^incrementcounter/$', view_increment_counter.incrementcounter, name='incrementcounter'),
                       url(r'^query/$', view_query.query, name='query'),
                       url(r'^suggest_code/$', view_suggest_code.suggest_code, name='suggest_code'),
                       url(r'^contact/$', view_contact.contact, name='contact'),
                       url(r'^about/$', view_about.about, name='about'),
                       url(r'^error/(?P<error_type>\w+)/$', view_error.error, name='error'),
                       url(r'^uploadphotograph/$', view_upload_photograph.upload_photograph, name='upload_photograph'),
                       url(r'^managephotographs/(?P<photo_id>\w+)/$', view_manage_photos.manage_photographs,
                           name='manage_photographs'),
                       url(r'^photo_select/$', view_photo_select.photo_select, name='select_photo'),
                       url(r'^sample_photos/$', view_sample_photos.sample_photos, name='sample_photos'),
                       url(r'^check_photofile/$', view_check_photofile.check_photofile, name='check_photofile'),
                       url(r'^createnew/(?P<sample_type_url>\w+)/$', view_create_new.create_new, name='create_new'),
                       )


