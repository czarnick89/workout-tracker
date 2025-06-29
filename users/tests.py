from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserRegistrationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')  # ensure your url name='register'
    
    def test_register_user_success(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'StrongPass123!'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User registered successfully')
        self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_register_user_missing_password(self):
        data = {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            # 'password' omitted
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data['error']['message'])
    
    def test_register_user_duplicate_username(self):
        User.objects.create_user(username='existinguser', password='StrongPass123!')
        data = {
            'username': 'existinguser',
            'email': 'newemail@example.com',
            'password': 'AnotherStrongPass123!'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data['error']['message'])

class LogoutTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='logoutuser', password='LogoutPass123!')
        self.logout_url = reverse('logout')
        refresh = RefreshToken.for_user(self.user)
        self.refresh_token = str(refresh)
        self.access_token = str(refresh.access_token)

    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(self.logout_url, {'refresh': self.refresh_token})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response.data['detail'], 'Logout successful')
    
    def test_logout_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(self.logout_url, {'refresh': 'invalidtoken'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid token')

class UserAuthTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='Password123!')
        self.login_url = reverse('token_obtain_pair')
        self.logout_url = reverse('logout')
        # Obtain tokens for the user
        response = self.client.post(self.login_url, {'username': 'alice', 'password': 'Password123!'})
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(self.logout_url, {'refresh': self.refresh_token})
        self.assertEqual(response.status_code, 205)
        self.assertEqual(response.data['detail'], 'Logout successful')

    def test_logout_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(self.logout_url, {'refresh': 'invalidtoken'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)