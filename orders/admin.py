from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Number of empty forms for new order items

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at', 'delivered_at')
    list_filter = ('status', 'created_at', 'is_cancelled', 'is_valid', 'is_delivered', 'is_returned')
    search_fields = ('user__first_name', 'user__last_name', 'status')
    inlines = [OrderItemInline]  # Adds inline management of OrderItem

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'subtotal')
    list_filter = ('order__status', 'product')
    search_fields = ('order__user__first_name', 'order__user__last_name', 'product__name')