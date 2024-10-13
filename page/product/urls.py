from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('', views.product_list, name='product_list'),
    path('product/add/review_to<int:product_id>/', views.add_review, name='add_review'),
    path('review/edit/<int:review_id>/', views.edit_review, name='review_edit'),
    path('reply/add/reply_to/<int:review_id>/', views.add_reply, name='reply_add'),
    path('reply/edit/<int:reply_id>/', views.edit_reply, name='reply_edit'),
    path('review/toggle_visibility/<int:review_id>/', views.toggle_visibility_review, name='review_toggle_visibility'),
    path('reply/toggle_visibility/<int:reply_id>/', views.toggle_visibility_reply, name='reply_toggle_visibility'),
    path('products_with_reviews/', views.product_review_options, name='review_manipulation'),
]
