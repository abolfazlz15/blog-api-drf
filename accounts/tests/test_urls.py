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

    def test_check_otp(self):
        url = reverse('accounts:check-otp')
        self.assertEqual(resolve(url).func.view_class, views.CheckOtpCodeView)

    def test_user_update(self):
        url = reverse('accounts:user-edit-profile')
        self.assertEqual(resolve(url).func.view_class, views.UpdateProfileView)

    def test_user_update_check_user(self):
        url = reverse('accounts:user-edit-profile-check-email')
        self.assertEqual(resolve(url).func.view_class, views.VerifyOTPView)                      