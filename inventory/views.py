from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, F, Count
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from .models import Product, Order, OrderItem
from .serializers import (
    ProductSerializer, OrderSerializer, 
    OrderStatusUpdateSerializer, OrderItemSerializer
)
from users.permissions import IsAdmin, IsUser

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
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
        if user.is_staff or user.is_admin:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        # Automatically set the user to the authenticated user
        serializer.save(user=self.request.user)

class UpdateOrderStatusView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAdmin]

@api_view(['GET'])
@permission_classes([IsAdmin])
def low_stock_report(request):
    threshold = int(request.query_params.get('threshold', '10'))
    try:
        threshold = int(threshold)
        if threshold <= 0:
            raise ValueError()
    except ValueError:
        return Response({"error": "Threshold must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

    low_stock_products = Product.objects.filter(quantity__lt=threshold)
    serializer = ProductSerializer(low_stock_products, many=True)
    return Response({
        'threshold': threshold,
        'count': low_stock_products.count(),
        'products': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAdmin])
def sales_report(request):
    period = request.query_params.get('period', 'day')
    
    # Define the truncation function based on the period
    if period == 'week':
        trunc_func = TruncWeek('order__created_at')
    elif period == 'month':
        trunc_func = TruncMonth('order__created_at')
    else:  # default to day
        trunc_func = TruncDate('order__created_at')
    
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