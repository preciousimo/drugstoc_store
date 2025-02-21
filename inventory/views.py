from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, F, Count
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, Order, OrderItem
from .serializers import (
    ProductSerializer, OrderSerializer, 
    OrderStatusUpdateSerializer
)
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

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UpdateOrderStatusView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAdminUser]

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def low_stock_report(request):
    """API endpoint to generate report of products with low stock"""
    threshold = request.query_params.get('threshold', 10)
    low_stock_products = Product.objects.filter(quantity__lt=threshold)
    serializer = ProductSerializer(low_stock_products, many=True)
    return Response({
        'threshold': threshold,
        'count': low_stock_products.count(),
        'products': serializer.data
    })

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def sales_report(request):
    """API endpoint to generate sales report by time period"""
    
    period = request.query_params.get('period', 'day')
    
    # Define the truncation function based on the period
    if period == 'week':
        trunc_func = TruncWeek('created_at')
    elif period == 'month':
        trunc_func = TruncMonth('created_at')
    else:  # default to day
        trunc_func = TruncDate('created_at')
    
    # Only consider completed orders
    completed_orders = Order.objects.filter(status='completed')
    
    # Get all order items from completed orders
    order_items = OrderItem.objects.filter(order__in=completed_orders)
    
    # Aggregate sales by period
    sales_by_period = order_items.annotate(
        period=trunc_func
    ).values(
        'period'
    ).annotate(
        total_sales=Sum(F('price_at_order') * F('quantity')),
        order_count=Count('order', distinct=True),
        units_sold=Sum('quantity')
    ).order_by('period')
    
    return Response({
        'period': period,
        'data': sales_by_period
    })