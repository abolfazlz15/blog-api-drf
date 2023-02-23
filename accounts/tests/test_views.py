import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.otp_service import OTP
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



class CheckOtpCodeViewTest(APITestCase):
    def setUp(self):
        # Set up any data needed for the test case
        self.url = reverse('accounts:check-otp')

        self.valid_data = {
            'code': '1234'
        }
        # Set up test user data for creating a user after OTP validation
        self.test_user_data = {
            'email': 'test@test.com',
            'full_name': 'Test User',
            'password': 'testpassword'
        }

def test_valid_otp_code(self):
    # Set up the cache with test data
    cache.set(key='register-otp', value=self.test_user_data)
    response = self.client.post(self.url, data=self.valid_data, format='json')
    if response.status_code == status.HTTP_200_OK:
        user_created = User.objects.filter(email=self.test_user_data['email']).exists()
        if user_created:
            # Check that a user was created with the correct data
            user = User.objects.get(email=self.test_user_data['email'])
            self.assertEqual(user.full_name, self.test_user_data['full_name'])
            self.assertTrue(user.check_password(self.test_user_data['password']))
            # Check that the register key was deleted from the cache
            self.assertIsNone(cache.get('register-otp'))
        else:
            self.fail("A user was not created after validating a valid OTP code.")
    else:
        self.fail("The OTP code was not valid.")


class UserProfileViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', full_name='testuser', password='testpass')
        self.url = reverse('accounts:user-profile')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def test_user_profile_view(self):
     
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['email'])
        self.assertEqual(json.loads(response.content), {'full_name': 'testuser', 'email': 'testuser@example.com'})



