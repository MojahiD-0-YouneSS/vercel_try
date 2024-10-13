from django.urls import path
from . import views
app_name = 'orders'

urlpatterns = [
    path('make_order/<int:product_id>/', views.make_order, name='make_order'),
    path('edit/order/<int:order_id>', views.edit_order, name='order_edit'),
    path('Delivered_Orders/', views.Delivered_Orders, name='Delivered_Orders'),
    path('Returned_Orders/', views.Returned_Orders, name='Returned_Orders'),
    path('Valid_Orders/', views.Valid_Orders, name='Valid_Orders'),
    path('Cancelled_Orders/', views.Cancelled_Orders, name='Cancelled_Orders'),
    path('delivered/order/<int:order_id>/', views.delivered_order, name='delivered'),
    path('validated/order/<int:order_id>/', views.valid_order, name='validated'),
    path('cancelled/order/<int:order_id>/', views.cancelled_order, name='cancelled'),
    path('returned/order/<int:order_id>/', views.returned_order, name='returned'),
]
