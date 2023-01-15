from django.urls import resolve, reverse
from rest_framework.test import APITestCase
from blog.api import views
from blog.models import Article
from accounts.models import User


class TestUrls(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@gmail.com', full_name='test', password='test1234')
        cls.article = Article.objects.create(
            title='article test', text='this is test description', author=cls.user)


    def test_article_list_url(self):
        url = reverse('blog:article-list')
        self.assertEqual(resolve(url).func.view_class, views.ArticleListView)

    def test_article_add_url(self):
        url = reverse('blog:article-add')
        self.assertEqual(resolve(url).func.view_class, views.ArticleAddView)

    def test_article_detail_url(self):
        url = reverse('blog:article-detail', args=(self.article.id,))
        self.assertEqual(resolve(url).func.view_class, views.ArticleDetailView)

    def test_article_delete_url(self):
        url = reverse('blog:article-delete', args=(self.article.id,))
        self.assertEqual(resolve(url).func.view_class, views.ArticleDeleteView)

    # def test_article_update_url(self):
    #     url = reverse('blog:article-update', args=(self.article.id,))
    #     self.assertEqual(resolve(url).func.view_class, views.ArticleUpdateView)    