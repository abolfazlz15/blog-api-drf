from django.contrib import admin

class LikeAdmin(admin.ModelAdmin):
    list_display = ('article', 'user')
    search_fields = ('article', 'user')
