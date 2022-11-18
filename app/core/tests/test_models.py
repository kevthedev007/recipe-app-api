from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
  def test_create_user_with_email(self):
    email = 'kev@example.com'
    password= 'test123'
    user = get_user_model().objects.create_user(email=email, password=password)
    
    self.assertEqual(user.email, email)
    self.assertTrue(user.check_password(password))
    
  def test_create_superuser(self):
    user = get_user_model().objects.create_superuser("kk@example.com", "test123")
    
    self.assertTrue(user.is_staff)
    self.assertTrue(user.is_superuser)
    
  def test_normalize_email(self):
    expected = 'test12@example.com'  
    user = get_user_model().objects.create_user('test12@EXAMPLE.com', 'test123')
    
    self.assertEqual(user.email, expected)