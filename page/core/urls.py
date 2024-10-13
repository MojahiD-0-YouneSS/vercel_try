from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('success/', views.success, name='success'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
