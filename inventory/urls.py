from django.urls import path
from . import views

urlpatterns = [
    
    # Products
    path('products', views.ProductViewSet.as_view({'get': 'list','post': 'create'}), name='product-list'),
    path('product/<uuid:pk>/', views.ProductViewSet.as_view({'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'}), name='product-detail'),
]