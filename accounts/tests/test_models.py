from django.utils.translation import gettext_lazy as _
from rest_framework.test import APITestCase

from accounts.models import User


class UserrModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email='test@example.com', full_name='test', password='1234')

    def test_email_label(self):
        field_label = self.user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, _('email address'))

    def test_full_name_label(self):
        field_label = self.user._meta.get_field('full_name').verbose_name
        self.assertEqual(field_label, _('full name'))

    def test_str_method(self):
        expected_result = self.user.email
        self.assertEqual(self.user.__str__(), expected_result)