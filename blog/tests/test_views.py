from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from blog.api import serializers
from blog.models import Article, Category, Tag
from rest_framework_simplejwt.tokens import RefreshToken


class ArticleListViewTestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title="category")
        self.user = User.objects.create_user(
            email='test@gmail.com', full_name='test', password='test1234')
        self.tag = Tag.objects.create(title="tag")
        self.article = Article.objects.create(
            title="Test article",
            text="Test text",
            status=True,
            category=self.category,
            author=self.user,
            tag=self.tag
        )

    def test_list_articles(self):
        url = reverse('blog:article-list')
        response = self.client.get(url)
        articles = Article.objects.filter(status=True)
        serializer = serializers.ArticleListSrializer(articles, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class ArticleDetailViewTestCase(APITestCase):
    @classmethod
    def setUp(self):
        self.category = Category.objects.create(title="category")
        self.user = User.objects.create_user(
            email='test@gmail.com', full_name='test', password='test1234')
        self.refresh = RefreshToken.for_user(self.user)
        self.token = str(self.refresh.access_token)
        self.tag = Tag.objects.create(title="tag")
        self.article = Article.objects.create(
            title="Test article",
            text="Test text",
            status=True,
            category=self.category,
            author=self.user,
            tag=self.tag
        )

    def test_get_article_detail_authorized(self):
        url = reverse('blog:article-detail', kwargs={'pk': self.article.id})
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        serializer = serializers.ArticleDetailSrializer(instance=self.article)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_article_detail_unauthorized(self):
        url = reverse('blog:article-detail', kwargs={'pk': self.article.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
