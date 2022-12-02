from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse('recipe:ingredient-list')

def detail_url(ingredient_id):
  return reverse('recipe:ingredient-detail', args=[ingredient_id])

def create_user(email='test@example.com', password='test123'):
  return get_user_model().objects.create_user(email, password)


class PublicIngredientsAPITests(TestCase):
  def setUp(self):
    self.client = APIClient()
    
  def test_auth_required(self):
    res = self.client.get(INGREDIENT_URL)
    
    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
    
class PrivateIngredientAPITests(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.user = create_user()
    self.client.force_authenticate(user=self.user)
    
  def test_retrieve_ingredients(self):
    Ingredient.objects.create(user=self.user, name='Kale')
    Ingredient.objects.create(user=self.user, name='Vanilla')
    
    res = self.client.get(INGREDIENT_URL)
    
    ingredients = Ingredient.objects.all().order_by('-name')
    serializer = IngredientSerializer(ingredients, many=True)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)
    
  def test_recipe_list_limited_to_user(self):
    other_user = create_user(email='test12@example.com', password='test1234')
    
    Ingredient.objects.create(user=other_user, name='Kale')
    Ingredient.objects.create(user=self.user, name='Vanilla')
    
    res = self.client.get(INGREDIENT_URL)
    
    ingredients = Ingredient.objects.filter(user=self.user)
    serializer = IngredientSerializer(ingredients, many=True)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)
    
  def test_update_ingredients(self):
    ingredient = Ingredient.objects.create(user=self.user, name='Kale')
    
    payload = { 'name': 'Coriandor' }
    url = detail_url(ingredient.id)
    res = self.client.patch(url, payload)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    ingredient.refresh_from_db()
    self.assertEqual(ingredient.name, payload['name'])
    
  def test_deelete_ingredient(self):
    ingredient = Ingredient.objects.create(user=self.user, name='Kale')
    
    url = detail_url(ingredient.id)
    res = self.client.delete(url)
    
    self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    ingredients = Ingredient.objects.filter(user=self.user)
    self.assertFalse(ingredients.exists())
    
  
    