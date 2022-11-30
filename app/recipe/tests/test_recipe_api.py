from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from core.models import Recipe
from decimal import Decimal
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
  return reverse('recipe:recipe-detail', args=[recipe_id])

def create_recipe(user, **params):
  defaults = {
    'title': 'Sample recipe',
    'description': 'sample recipe description',
    'price': Decimal('5.25'),
    'time_minutes': 25,
    'link': 'https://example.com/recipe.pdf'
  }
  defaults.update(params)
  recipe = Recipe.objects.create(user=user, **defaults)
  return recipe

def create_user(**params):
  return get_user_model().objects.create_user(**params)



class PublicRecipeAPITests(TestCase):
  def setUp(self):
    self.client = APIClient()
    
  def test_auth_required(self):
    res = self.client.get(RECIPES_URL)
    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    
class PrivateRecipeAPITests(TestCase):
  def setUp(self):
    self.user = create_user(email='kev@example.com', password='test1234')
    self.client =APIClient()
    self.client.force_authenticate(user=self.user)
    
  def test_retrieve_recipes(self):
    create_recipe(user=self.user)
    create_recipe(user=self.user)
    
    res = self.client.get(RECIPES_URL)
    
    recipes = Recipe.objects.all().order_by('-id')
    serializer = RecipeSerializer(recipes, many=True)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)
    
  def test_recipe_list_limited_to_user(self):
    other_user = create_user(email='test@example.com', password='test1234')
    
    create_recipe(user=other_user)
    create_recipe(user=self.user)
    
    res = self.client.get(RECIPES_URL)
    
    recipes = Recipe.objects.filter(user=self.user)
    serializer = RecipeSerializer(recipes, many=True)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)
    
  def test_get_recipe_detail(self):
    recipe = create_recipe(user=self.user)
    
    url = detail_url(recipe.id)
    res = self.client.get(url)
    
    serializer = RecipeDetailSerializer(recipe)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)
    
  def test_create_recipe(self):
    payload = {
      'title': 'recipe title',
      'time_minutes': 30,
      'price': Decimal('3.88')
    }
    
    res = self.client.post(RECIPES_URL, payload)
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    
    recipe = Recipe.objects.get(id = res.data['id'])
    
  def test_partial_update(self):
    original_link = 'https://example.com/recipe.pdf'
    recipe = create_recipe(
      user=self.user,
      title='sample recipe title',
      link=original_link,
    )
    payload = { 'title': 'new recipe title'}
    url = detail_url(recipe.id)
    
    res = self.client.patch(url, payload)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    recipe.refresh_from_db()
    self.assertEqual(recipe.title, payload['title'])
    self.assertEqual(recipe.link, original_link)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    
  
  def test_full_update(self):
    recipe = create_recipe(
      user=self.user,
      title='sample recipe title',
      link='https://example.com/recipe.pdf',
      description='sample recipe description'
    )
    
    payload = { 
      'title': 'new recipe title',
      'link': 'https://example/new-recipe.pdf',
      'description': 'new recipe description',
      'time_minutes': 10,
      'price': Decimal('4.90')        
    }
    
    url = detail_url(recipe.id)
    res = self.client.put(url, payload)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    recipe.refresh_from_db()
    for k,v in payload.items():
      self.assertEqual(getattr(recipe, k), v)
    self.assertEqual(recipe.user, self.user)
    
  def test_delete_recipe(self):
    recipe = create_recipe(user=self.user)
    
    url = detail_url(recipe.id)
    
    res = self.client.delete(url)
    self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)