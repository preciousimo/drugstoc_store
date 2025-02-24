from django.contrib import admin
from .models import Product, Order, OrderItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'quantity', 'price', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'updated_at', 'total_amount')
    search_fields = ('user__username', 'status')
    list_filter = ('status', 'created_at', 'updated_at')
    inlines = [OrderItemInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)