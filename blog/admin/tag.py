from django.contrib import admin

class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title',)
    ordering = ('created_at',)
