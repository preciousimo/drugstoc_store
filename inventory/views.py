from rest_framework import viewsets, permissions
from .models import Product
from inventory.serializers import ProductSerializer
from users.permissions import IsAdmin, IsUser


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        """
        Regular users can list and retrieve products but not modify
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]
