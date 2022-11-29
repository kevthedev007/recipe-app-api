from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")
CREATE_TOKEN_URL = reverse("user:token_obtain_pair")
ME_URL = reverse("user:me")

# Create your tests here.
class PublicUserAPITests(TestCase): 
  def setUp(self):
    self.client = APIClient()
    
  def test_create_user_success_message(self):
    payload = {
      'email': 'test@example.com',
      'password': 'test123',
      'password2': 'test123',
      'name': 'Test Name',
    }
    
    res = self.client.post(CREATE_USER_URL, payload)
    
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    
    user = get_user_model().objects.get(email=payload['email'])
    self.assertTrue(user.check_password(payload['password']))
    
  def test_duplicate_email_error(self):
    payload = {
      'email': 'test@example.com',
      'password': 'test123',
      'password2': 'test123',
      'name': 'Test Name',
    }
    
    user_payload = {
      'email': 'test@example.com',
      'password': 'test123',
      'name': 'Test Name',
    }
    
    get_user_model().objects.create_user(**user_payload)
    res = self.client.post(CREATE_USER_URL, payload)
    
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
  def test_user_get_access_token(self):
    payload = {
      'email': 'test@example.com',
      'password': 'test123',
      'name': 'Test Name',
    }
    
    tokenpayload = {
      'email': 'test@example.com',
      'password': 'test123',
    }
      
    get_user_model().objects.create_user(**payload)
    
    res = self.client.post(CREATE_TOKEN_URL, tokenpayload)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertIn('access', res.data)
    self.assertIn('refresh', res.data)
    
  def test_retrieve_user_unauthorized(self):
    res = self.client.get(ME_URL)
    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    

class PrivateUserAPITests(TestCase):
  '''Test API requests that requires authentication'''
  def setUp(self):
    self.user = get_user_model().objects.create_user(
      email='test@example.com',
      password='test123',
      name='Test Name'
    )
    self.client = APIClient()
    self.client.force_authenticate(user=self.user)
    
  def test_retrieve_profile_success(self):
    res = self.client.get(ME_URL)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, {
      'name': self.user.name,
      'email': self.user.email
    })
    
  def test_post_me_not_allowed(self):
    res = self.client.post(ME_URL, {})
    self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
  def update_me_profile(self):
    payload = {
      'name': 'updated user',
      'password': 'test456',
      'password2': 'test456'
    }
    
    res = self.client.patch(ME_URL, payload)
    
    self.user.refresh_from_db()
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(self.user.name, payload['name'])
    self.assertTrue(self.check_password(payload['password']))
  