from django.urls import path
from blog.api import views


app_name = 'blog'
urlpatterns = [
    path('articles', views.ArticleListView.as_view(), name='article-list')
]