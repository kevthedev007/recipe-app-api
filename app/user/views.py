from rest_framework import generics
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import UserSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt import authentication

# Create your views here.
#Register View
class RegisterUserView(generics.CreateAPIView):
  serializer_class = UserSerializer
  
#Login View
class EmailTokenObtainPairView(TokenObtainPairView):
  serializer_class = TokenObtainPairSerializer
  
class ManageUserView(generics.RetrieveUpdateAPIView):
  serializer_class = UserSerializer
  authentication_classes = [authentication.JWTAuthentication]
  permission_classes = [permissions.IsAuthenticated]
  
  def get_object(self):
    return self.request.user
  
