from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer

class PurchaseOrderCreateView(generics.CreateAPIView):
    queryset = PurchaseOrder.objects.all()  # Initial queryset
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def get_queryset(self):
        user = self.request.user  # Retrieve the authenticated user
        return PurchaseOrder.objects.filter(organization=user.organization)  # Filter by user's organization