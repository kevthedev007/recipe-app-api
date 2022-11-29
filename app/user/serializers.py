from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
  password2 = serializers.CharField(min_length=4, write_only=True)
  
  class Meta:
    model = get_user_model()
    fields = ['name', 'email', 'password', 'password2']
    extra_kwargs = {
      'password': { 'write_only':True, 'min_length': 4 }
    }
    
  def validate(self, attrs):
    password = attrs.get('password', None)
    if password:
      password2 = attrs.get('password')
      if not password2:
        raise serializers.ValidationError('Password must be provided')
      if attrs['password'] != attrs['password2']:
        raise serializers.ValidationError('Passwords do not match')
      password2 = attrs.pop('password2')
    return attrs
    
  def create(self, validated_data):
    return get_user_model().objects.create_user(**validated_data)
  
  def update(self, instance, validated_data):
    password = validated_data.pop('password', None)
    user = super().update(instance, validated_data)
    
    if password:
      user.set_password(password)
      user.save()
      
    return user
  
class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
  username_field = get_user_model().USERNAME_FIELD