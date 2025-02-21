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
    trunc_func = {
        'week': TruncWeek('created_at'),
        'month': TruncMonth('created_at'),
    }.get(period, TruncDate('created_at'))

    sales_by_period = (
        OrderItem.objects
        .filter(order__status='completed')
        .annotate(period=trunc_func)
        .values('period')
        .annotate(
            total_sales=Sum(F('price_at_order') * F('quantity')),
            order_count=Count('order', distinct=True),
            units_sold=Sum('quantity')
        )
        .order_by('period')
    )

    return Response({
        'period': period,
        'data': list(sales_by_period)
    })