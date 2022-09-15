from django.contrib import admin

from blog.admin.article import ArticleAdmin
from blog.admin.comment import CommentAdmin
from blog.admin.tag import TagAdmin
from blog.admin.like import LikeAdmin
from blog.admin.category import CategoryAdmin

from blog.models import (
    Article as ArticleModel,
    Comment as CommentModel,
    Category as CategryModel,
    Like as LikeModel,
    Tag as TagModel,
)

admin.site.register(ArticleModel, ArticleAdmin)
admin.site.register(CommentModel, CommentAdmin)
admin.site.register(CategryModel, CategoryAdmin)
admin.site.register(LikeModel, LikeAdmin)
admin.site.register(TagModel, TagAdmin)
