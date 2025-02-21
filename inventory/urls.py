from django.urls import path
from . import views

urlpatterns = [
    
    # Products
    path('products', views.ProductViewSet.as_view({'get': 'list','post': 'create'}), name='product-list'),
    path('product/<uuid:pk>/', views.ProductViewSet.as_view({'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'}), name='product-detail'),
    
    # Orders
    path('orders', views.OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='order-list'),
    path('order/<uuid:pk>/', views.OrderViewSet.as_view({'get': 'retrieve','put': 'update','delete': 'destroy'}), name='order-detail'),
    path('order/<uuid:pk>/status/', views.UpdateOrderStatusView.as_view(), name='update-order-status'),
    
    # Reports
    path('reports/low-stock/', views.low_stock_report, name='low-stock-report'),
    path('reports/sales/', views.sales_report, name='sales-report'),
]