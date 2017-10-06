from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.models import Permission

admin.site.register(User, UserAdmin)
admin.site.register(Permission)