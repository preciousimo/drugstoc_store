from django.urls import path

from . import views

urlpatterns = [
    
    # Users
    path('users', views.UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('user/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),
]