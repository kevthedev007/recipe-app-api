from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


class RecipeViewSet(ModelViewSet):
  queryset = Recipe.objects.all()
  serializer_class = RecipeDetailSerializer
  authentication_classes = [JWTAuthentication]
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