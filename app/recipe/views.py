from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import (
  RecipeSerializer, 
  RecipeDetailSerializer,
  TagSerializer, 
  IngredientSerializer,
)


class RecipeViewSet(ModelViewSet):
  '''View for managing Recipe APIs'''
  queryset = Recipe.objects.all()
  serializer_class = RecipeDetailSerializer
  sauthentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]
  lookup_field = 'pk'
  
  def get_queryset(self):
    return self.queryset.filter(user=self.request.user).order_by('-id')
  
  def get_serializer_class(self):
    if self.action == 'list':
      return RecipeSerializer
    return self.serializer_class
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)
    

class RecipeBaseAttrViewSet(
  mixins.ListModelMixin,
  mixins.UpdateModelMixin,
  mixins.DestroyModelMixin,
  GenericViewSet
):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user).order_by('-name')
  
  
class TagViewSet(RecipeBaseAttrViewSet):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer

class IngredientViewSet(RecipeBaseAttrViewSet):
  queryset = Ingredient.objects.all()
  serializer_class = IngredientSerializer
  