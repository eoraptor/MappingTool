from django.contrib import admin
#from django.contrib.auth.models import User
from mappingapp.models import Sample


class SampleAdmin(admin.ModelAdmin):
    list_display = ('sample_code', 'sample_location_name')


admin.site.register(Sample, SampleAdmin)
