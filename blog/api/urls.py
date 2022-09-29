from django.urls import path
from blog.api import views


app_name = 'blog'
urlpatterns = [
    path('articles', views.ArticleListView.as_view(), name='article-list'),
    path('articles/add', views.ArticleAddView.as_view(), name='article-list'),
    path('articles/<int:pk>', views.ArticleDetailView.as_view(), name='article-detail'),
    path('articles/update/<int:pk>', views.ArticleUpdateView.as_view(), name='article-update'),
    path('articles/delete/<int:pk>', views.ArticleDeleteView.as_view(), name='article-delete'),
]