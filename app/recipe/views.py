from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import (
  RecipeSerializer, 
  RecipeDetailSerializer,
  TagSerializer, 
  IngredientSerializer,
  RecipeImageSerializer,
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
    if self.action == 'upload_image':
      return RecipeImageSerializer
    return self.serializer_class
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)
    
  @action(methods=['POST'], detail=True, url_path='upload-image')
  def upload_image(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
    

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
  