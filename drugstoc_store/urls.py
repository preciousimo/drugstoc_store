from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from users.views import UserViewSet, CustomTokenObtainPairView, CustomTokenRefreshView, logout_view

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('api/', views.redirect_to_landing, name='redirect_to_landing'),
    
    # Admin URL patterns
    path('admin/', admin.site.urls),

    # Authentication URL patterns
    path('api/register', UserViewSet.as_view({'post': 'register'}), name='register'),  # Register a new user
    path('api/login', CustomTokenObtainPairView.as_view(), name='token_obtain'),  # Obtain a token for a user
    path('api/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),  # Refresh a token for a user
    path('api/logout', logout_view, name='logout'),

    # Other app URL patterns
    path('api/', include('users.urls')),
    path('api/', include('inventory.urls')),
]