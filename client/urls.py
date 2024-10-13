from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('info/<int:product_id>/', views.client_info, name='add_info'),
]
