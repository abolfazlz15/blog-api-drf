from django.contrib import admin


class OtpAdmin(admin.ModelAdmin):
    search_fields = ['email']
    list_display = ['id', 'email', 'code', 'expiration_date']
    list_filter = ['expiration_date']