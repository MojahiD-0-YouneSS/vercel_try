from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import user_passes_test, login_required

from datetime import timedelta
from django.utils import timezone
from django.db.models import Q

from client.models import Client
from orders.models import Order, OrderItem
from product.models import Product, Review

# Create your views here.
@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def Home_rachid_interface(request):
    pending_orders = Order.objects.filter(status='Pending').count()
    return render(request,'Rachid/rachid_interface.html', {'title':'Home', 'pending_orders':pending_orders}) 

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def Dashboard_rachid_interface(request):
    low_stock_products = Product.objects.filter(quantity__lte=15).count()
    newest_orders = Order.objects.filter(created_at__gte=timezone.now() - timedelta(days=7)).count()
    # count created session for user
    recent_contacts_made_by_call = Order.objects.filter( Q(is_cancelled=True) | Q(is_valid=True) | Q(is_returned=True)  | Q(is_delivered=True)).count()
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now()).count()
    cancelled_order = Order.objects.filter(is_cancelled=True).count()
    valid_order = Order.objects.filter(is_valid=True).count()
    pending_orders = Order.objects.filter(status='Pending').count()
    context = {
        'title':'Dashboard',
        'low_stock_products':low_stock_products,
        'newest_orders':newest_orders,
        'recent_contacts_made_by_call':recent_contacts_made_by_call,
        'recent_visitors':active_sessions,
        'cancelled_orders':cancelled_order,
        'valid_orders':valid_order,
        'pending_orders':pending_orders,
    }
    return render(request,'Rachid/rachid_interface.html', context) 

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def Orders_rachid_interface(request):
    def update_orders_subtotal():
        orders = Order.objects.filter(status='Pending')
        for order in orders:
            order.fix_status().filling_thegap()
        return None
    update_orders_subtotal()
    orders = Order.objects.filter(status='Pending')
    pending_orders = orders.count()
    context = {
        'title':'Orders',
        'orders':orders,
        'pending_orders':pending_orders,
    }

    return render(request,'Rachid/rachid_interface.html', context) 

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def Products_rachid_interface(request):
    context = {
        'title':'Products',
    }

    return render(request,'Rachid/rachid_interface.html', context) 

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def Visitors_rachid_interface(request):
    total_visitors = Session.objects.all().count()
    total_visitors_with_same_devise = 0 
    sessions = Session.objects.all()

    for session in sessions:
        session_data = session.get_decoded()
        if 'anonymos_user_id' in session_data:
           total_visitors_with_same_devise += 1
    total_orderd_visitors = Client.objects.values('phone').distinct().count()
    total_visitors_not_ordered = total_visitors - total_visitors_with_same_devise if total_visitors > total_visitors_with_same_devise else 0
    pending_orders = Order.objects.filter(status='Pending').count()

    context = {
        'title':'Visitors',
        'total_visitors':total_visitors,
        'total_orderd_visitors':total_orderd_visitors,
        'total_visitors_not_ordered':total_visitors_not_ordered,
        'total_visitors_with_same_devise':total_visitors_with_same_devise,
        'pending_orders':pending_orders,
    }
    return render(request,'Rachid/rachid_interface.html', context) 

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def CMVC_rachid_interface(request):
    orders = Order.objects.filter(
        Q(is_cancelled=True) | 
        Q(is_delivered=True) | 
        Q(is_valid=True) | 
        Q(is_returned=True)
    )
    pending_orders = Order.objects.filter(status='Pending').count()
    context = {
        'title':'contacts made via calls',
        'orders':orders,
        'total_calls' : orders.count(),
        'pending_orders':pending_orders,
    }

    return render(request,'Rachid/rachid_interface.html', context) 
