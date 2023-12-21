from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from dj_rest_auth import views 
from . views import CustomRegistrationView



# ... other dj-rest-auth views

urlpatterns = [
    path('register/',CustomRegistrationView.as_view(),name='register'),
    path('login/',TokenObtainPairView.as_view(),name='login') ,
    path('token/refresh/',TokenRefreshView.as_view(),name='token-refresh')
    # ... other app URLs
]