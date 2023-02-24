from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from blog.api import serializers
from blog.models import Article, Category, Tag

from rest_framework.test import APIClient

class ArticleListViewTestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title='category')
        self.user = User.objects.create_user(
            email='test@gmail.com', full_name='test', password='test1234')
        self.tag = Tag.objects.create(title='tag')
        self.article = Article.objects.create(
            title='Test article',
            text='Test text',
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
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        serializer = serializers.ArticleDetailSrializer(instance=self.article)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_article_detail_unauthorized(self):
        url = reverse('blog:article-detail', kwargs={'pk': self.article.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ArticleUpdateViewTest(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            email='test@gmail.com', full_name='test', password='test1234')
        self.refresh = RefreshToken.for_user(self.user)
        self.token = str(self.refresh.access_token)
        self.category = Category.objects.create(title='Test Category')
        self.tag = Tag.objects.create(title="tag")
        self.article = Article.objects.create(
            title='Test Article', author=self.user, category=self.category, status=True)
        self.new_data = {
            'title': 'test update',
            'text': 'this is test article update',
        }

    def test_update_article_authorized(self):
        url = reverse('blog:article-update', args=(self.article.id,))

        response = self.client.put(
            url, data=self.new_data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_article_update_unauthorized(self):
        url = reverse('blog:article-update', args=(self.article.id,))

        response = self.client.put(url, data=self.new_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ArticleDeleteViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@gmail.com', full_name='test', password='test1234')
        self.article = Article.objects.create(
            title='Test Article', author=self.user, status=True)
        self.refresh = RefreshToken.for_user(self.user)
        self.token = str(self.refresh.access_token)
        self.url = reverse('blog:article-delete', args=(self.article.id,))

    def test_delete_article(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Article.objects.filter(pk=self.article.pk).exists())

    def test_delete_article_unauthorized(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Article.objects.filter(pk=self.article.pk).exists())

    def test_delete_article_not_author(self):
        other_user = User.objects.create_user(
            email='other@example.com', full_name='otheruser', password='othertest1234')
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Article.objects.filter(pk=self.article.pk).exists())


