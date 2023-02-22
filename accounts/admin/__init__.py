from django.contrib import admin

from accounts.admin.user import UserAdmin

from accounts.models import (
    User as UserModel,
)

admin.site.register(UserModel, UserAdmin)
