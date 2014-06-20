from django.contrib import admin
from django.contrib.auth.models import User
from mappingapp.models import UserProfile


admin.site.register(UserProfile)
