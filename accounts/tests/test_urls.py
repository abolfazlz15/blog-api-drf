from django.urls import resolve, reverse
from rest_framework.test import APISimpleTestCase

from accounts.api import views


class TestUrls(APISimpleTestCase):
    def test_login(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func.view_class, views.UserLoginView)

    def test_register(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func.view_class, views.UserRegisterView)
    
    def test_user_profile(self):
        url = reverse('accounts:user-profile')
        self.assertEqual(resolve(url).func.view_class, views.UserProfileView)

