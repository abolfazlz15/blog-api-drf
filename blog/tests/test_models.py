from django.utils.translation import gettext_lazy as _
from rest_framework.test import APITestCase

from accounts.models import User
from blog.models import Article, Category, Tag


class ArticleModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@example.com', full_name='test', password='1234')
        cls.category = Category.objects.create(title='category')
        cls.tag = Tag.objects.create(title='tag')
        cls.article = Article.objects.create(
            title='Test article',
            text='Test text',
            status=True,
            category=cls.category,
            author=cls.user,
            tag=cls.tag
        )

    def test_title_label(self):
        field_label = self.article._meta.get_field('title').verbose_name
        self.assertEqual(field_label, _('Title'))

    def test_text_label(self):
        field_label = self.article._meta.get_field('text').verbose_name
        self.assertEqual(field_label, _('Description'))

    def test_status_label(self):
        field_label = self.article._meta.get_field('status').verbose_name
        self.assertEqual(field_label, _('Status'))

    def test_iamge_label(self):
        field_label = self.article._meta.get_field('image').verbose_name
        self.assertEqual(field_label, _('Image'))

    def test_str_method(self):
        expected_result = f'{self.article.title} - {self.article.text[:20]}'
        self.assertEqual(self.article.__str__(), expected_result)


class TagTestCase(APITestCase):
    @classmethod
    def setUp(cls):
        cls.tag = Tag.objects.create(title="Test Tag")

    def test_title_lable(self):
        field_label = self.tag._meta.get_field('title').verbose_name
        self.assertEqual(field_label, _('Title'))

    def test_created_at_label(self):
        field_label = self.tag._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, _('Created at'))

    def test_tag_str(self):
        tag = Tag.objects.get(title="Test Tag")
        self.assertEqual(str(tag), "Test Tag")


class CategoryTestCase(APITestCase):
    @classmethod
    def setUp(cls):
        cls.category = Category.objects.create(title="Test Category")

    def test_title_lable(self):
        field_label = self.category._meta.get_field('title').verbose_name
        self.assertEqual(field_label, _('Title'))
        
    def test_created_at_label(self):
        field_label = self.category._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, _('Created at'))

    def test_category_str(self):
        category = Category.objects.get(title="Test Category")
        self.assertEqual(str(category), "Test Category")        