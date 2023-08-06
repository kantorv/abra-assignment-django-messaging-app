from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    pass