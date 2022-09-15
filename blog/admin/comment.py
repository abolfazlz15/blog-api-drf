from django.contrib import admin


class CommentAdmin(admin.ModelAdmin):
    search_fields = ['article', 'user', 'text']
    list_display = ['id', 'article', 'user', 'parent']
    list_filter = ['status', 'created_at']