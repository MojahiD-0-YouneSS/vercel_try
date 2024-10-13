from django.urls import path
from . import views
app_name = 'Rachid'
# rhome == rachid's (owner) home not the client
urlpatterns = [
    path("Home/", views.Home_rachid_interface, name="rhome"),
    path("dashboard/", views.Dashboard_rachid_interface, name="dashboard"),
    path("orders/", views.Orders_rachid_interface, name="rorders"),
    path("visitors/", views.Visitors_rachid_interface, name="rvisitors"),
    path("contacts_made_via_calls/", views.CMVC_rachid_interface, name="cmvc"),
    path("products/", views.Products_rachid_interface, name="rproducts"),
]
