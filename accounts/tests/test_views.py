from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core import mail
from django.core.cache import cache
from unittest.mock import patch

User = get_user_model()

class UserLoginViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            full_name = 'test',
            password='testpassword',
        )
        self.valid_payload = {
            'email': 'test@example.com',
            'full_name': 'test',
            'password': 'testpassword'
        }
        self.invalid_payload = {
            'email': 'test@example.com',
            'full_name': 'test',
            'password': 'invalidpassword'
        }

    def test_login_with_valid_credentials(self):
        url = reverse('accounts:login')
        response = self.client.post(
            url,
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_login_with_invalid_credentials(self):
        url = reverse('accounts:login')
        response = self.client.post(
            url,
            data=self.invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserRegisterViewTest(APITestCase):
    def test_register_user(self):
        email = 'test@example.com'
        password = 'strongpassword'
        full_name = 'Test User'

        with patch('accounts.otp_service.OTP.generate_otp') as generate_otp_mock:
            url = reverse('accounts:register')
            response = self.client.post(url, {'email': email, 'password': password, 'full_name': full_name})
            self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
            self.assertEqual(response.data, {'email': email, 'result': 'email sended'})

            # Assert that OTP was generated and email was sent


            # Assert that user data was cached
            cached_user_data = cache.get('register')
            self.assertEqual(cached_user_data, {'email': email, 'password': password, 'full_name': full_name})

    def test_invalid_data(self):
        url = reverse('accounts:register')
        response = self.client.post(url, {'email': 'test@example.com', 'password': 'weak', 'full_name': 'Test User'})
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertNotIn('email', response.data)
        self.assertIn('password', response.data)
        self.assertNotIn('full_name', response.data)

        # Assert that OTP was not generated and email was not sent


        # Assert that user data was not cached
        cached_user_data = cache.get('register')
        self.assertIsNone(cached_user_data)
