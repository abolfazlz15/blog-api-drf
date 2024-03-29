from django.urls import path
from blog.api import views


app_name = 'blog'
urlpatterns = [
    path('articles', views.ArticleListView.as_view(), name='article-list'),
    path('articles/add', views.ArticleAddView.as_view(), name='article-add'),
    path('articles/<int:pk>', views.ArticleDetailView.as_view(), name='article-detail'),
    path('articles/update/<int:pk>', views.ArticleUpdateView.as_view(), name='article-update'),
    path('articles/delete/<int:pk>', views.ArticleDeleteView.as_view(), name='article-delete'),
    
    # category URl
    path('category/add', views.CategoryAddView.as_view(), name='category-add'),
    path('category', views.CategoryListView.as_view(), name='category-list'),
    path('category/delete/<int:pk>', views.CategoryDeleteView.as_view(), name='category-delete'),
    
    # Comment URL
    path('comment/add', views.CommentAddView.as_view(), name='comment-add'),
    
    path('author', views.AuthorListView.as_view(), name='author-list'),
]