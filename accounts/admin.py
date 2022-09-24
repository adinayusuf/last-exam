from django.contrib.auth.admin import UserAdmin

from accounts.models import Profile
from django.contrib import admin


class ProfileAdmin(UserAdmin):
    pass

admin.site.register(Profile,ProfileAdmin)
