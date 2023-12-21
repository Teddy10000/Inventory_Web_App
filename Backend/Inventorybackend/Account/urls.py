from rest_framework import routers
from django.urls import path, include

from dj_rest_auth import views 
from . views import CustomRegistrationView



# ... other dj-rest-auth views

urlpatterns = [
    path('register/',CustomRegistrationView.as_view(),name='register'),
    # ... other app URLs
]