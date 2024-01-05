from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated , DjangoModelPermissions
from django.core.exceptions import PermissionDenied
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from django.shortcuts import get_object_or_404




#THIS THE PURCAHSE ORDER CREATE VIEW 
class PurchaseOrderCreateView(generics.CreateAPIView):
     # Initial queryset
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def get_queryset(self):
        user = self.request.user  # Retrieve the authenticated user
        return PurchaseOrder.objects.filter(organization=user.organization)  # Filter by user's organization
    
class PurchaseOrderListView(generics.ListAPIView):
    serializer_class = PurchaseOrderSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if user.organization is None:
            raise PermissionDenied("You must be belong to an Organization to view purcahse orders")
        return PurchaseOrder.objects.filter(organization=user.organization)
    
class PurchaseOrderDetailedView(generics.RetrieveAPIView):
    serializer_class = PurchaseOrderSerializer
    permission_classes =  [DjangoModelPermissions]
    lookup_field = 'pk'

    def get_queryset(self):
            user = self.request.user
            if user.organization is None:
                raise PermissionDenied("You must be belong to an Organization to view purcahse orders")
            return PurchaseOrder.objects.filter(organization=user.organization)

class PurchaseOrderUpdateView(generics.UpdateAPIView):
     serializer_class = PurchaseOrderSerializer
     permission_classes = [DjangoModelPermissions]
     lookup_field = 'pk'

     def get_queryset(self):
            user = self.request.user
            if user.organization is None:
                raise PermissionDenied("You must be belong to an Organization to view purcahse orders")
            return PurchaseOrder.objects.filter(organization=user.organization)


     def get_object(self):
        queryset = super().get_queryset()  # Apply any filtering from get_queryset
        purchase_order = get_object_or_404(queryset, pk=self.kwargs['pk'])

        # Organization check (as before)
        if purchase_order.organization != self.request.user.organization:
            raise PermissionDenied("You are not authorized to access this purchase order.")

        # Creator check
        if purchase_order.created_by != self.request.user:
            raise PermissionDenied("Only the creator of the purchase order can update it.")

        return purchase_order
     
     def update(self, request, *args, **kwargs):
        purchase_order = self.get_object()  # Retrieve purchase order

        # Update logic, handle serializer and validations

        if purchase_order.updated_by != self.request.user:
            raise PermissionDenied("Only the user who last updated this purchase order can update it.")

        return super().update(request, *args, **kwargs)