from django.contrib import admin

from accounts.admin.otp import OtpAdmin
from accounts.admin.user import UserAdmin

from accounts.models import (
    User as UserModel,
    OTPCode as OtpCodeModel,
)

admin.site.register(UserModel, UserAdmin)
admin.site.register(OtpCodeModel, OtpAdmin)