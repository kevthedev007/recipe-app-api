from django.db import models
from django.contrib.auth.models import (
  AbstractBaseUser,
  PermissionsMixin,
  BaseUserManager
)
from django.conf import settings

# Create your models here.
class UserManager(BaseUserManager):
  def create_user(self, email, password, **extra_fields):
    if not email:
      ValueError("Email must be inputed")
    if not password:
      ValueError("Password must be present")
    user = self.model(email=self.normalize_email(email), **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self, email, password, **extra_fields):
    user = self.create_user(email, password)
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user
  

class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(max_length=255, unique=True)
  password = models.CharField(max_length=255)
  name = models.CharField(max_length=255)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  
  objects = UserManager()
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []
  
  
class Recipe(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  time_minutes = models.IntegerField()
  price = models.DecimalField(max_digits=5, decimal_places=2)
  link = models.CharField(max_length=255, blank=True)
  tags = models.ManyToManyField('Tag')
  ingredients = models.ManyToManyField('Ingredient')
  
  def __str__(self):
    return self.title
  

class Tag(models.Model):
  name = models.CharField(max_length=255)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.name
  
  
class Ingredient(models.Model):
  name = models.CharField(max_length=255)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.name
