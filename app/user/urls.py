from django.urls import path
from user.views import RegisterUserView, EmailTokenObtainPairView, ManageUserView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'user'

urlpatterns = [
  path('create/', RegisterUserView.as_view(), name='create'),
  path('token/obtain/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('me/', ManageUserView.as_view(), name='me'),
]