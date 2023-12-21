from django.shortcuts import render
from . serializers import CustomRegistrationSerializer
# Create your views here.
from dj_rest_auth.registration.views import RegisterView

class CustomRegistrationView(RegisterView):
    serializer_class = CustomRegistrationSerializer
