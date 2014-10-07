from django.contrib import admin
#from django.contrib.auth.models import User
from mappingapp.models import Sample_Site


class Sample_SiteAdmin(admin.ModelAdmin):
    list_display = ('collected_by', 'site_name', 'site_location', 'county', 'site_date', 'operator',
    'geomorph_setting', 'sample_type_collected', 'photos_taken', 'photographs', 'site_notes')


admin.site.register(Sample_Site, Sample_SiteAdmin)
