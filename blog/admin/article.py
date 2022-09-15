from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('showImage', 'title', 'status', 'author')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'text', 'author')
    ordering = ('created_at',)
