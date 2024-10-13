from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.mail import send_mail
from django.conf import settings
from . import models as M
from client.models import Client
from .forms import EditOrderForm, OrderItemFormSet
from product.models import Product
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_order_notification(order):
    subject = f'New Order Placed: Order ID {order.id}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [settings.MANAGER_EMAIL]

    items  = M.OrderItem.objects.filter(order=order)
    context = {
        'order_id': order.id,
        'customer_name': f'{order.user.full_name}',
        'customer_phone': f'{order.user.phone}',
        'products': items,
        'total_price': (items.first().quantity * items.first().product.promotion_price),  # Assuming you have a method
        'order_date': order.created_at,
    }

    html_content = render_to_string('order/email.html', context)
    
    text_content = f'A new order has been placed: \nclient : {order.user.full_name}.\nPhone : {order.user.phone}.\nOrder ID: {order.id}\nPlease process the order as soon as possible.'

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()
    return order

def make_order(request, product_id, user_quantity=1):
    user_id = request.session.get('anonymos_user_id', '')
    product = get_object_or_404(Product, id=product_id)
    product.quantity -= user_quantity
    product.save()
    user = get_object_or_404(Client, id=user_id)
    order , created= M.Order.objects.get_or_create(user=user,)
    order.filling_thegap()
    
    order_item = M.OrderItem.objects.create(
                order=order,
                product=product,
                quantity=user_quantity
            )
    order_item.subtotal_calculation()
    
    send_order_notification(order)

    url = reverse('core:home')
    success_url = f"{reverse('core:success')}?redirect_url={url}"
    
    return redirect(success_url)
    
@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def edit_order(request, order_id):
    order = get_object_or_404(M.Order, id=order_id)
    if request.method == 'POST':
        form = EditOrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        
        if form.is_valid() and formset.is_valid():
            form.save()  # Save the Order
            formset.save()  # Save the associated OrderItems
            return redirect('Rachid:rorders')  # Redirect after saving
    else:
        form = EditOrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)
    
    return render(request, 'order/edit_order.html', {
        'form': form,
        'formset': formset,
    })


@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def valid_order(request, order_id):
    order = get_object_or_404(M.Order, id=order_id)
    order.is_valid = True
    order.is_cancelled = False
    order.is_returned = False
    order.is_delivered = False
    order.status = order.STATUS_CHOICES[1][1]
    order.save()
    for item in order.orderitem_set.all():
        item.subtotal_calculation()

    return redirect('Rachid:rorders')

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def returned_order(request, order_id):
    order = get_object_or_404(M.Order, id=order_id)
    order.is_returned = True
    order.is_cancelled = False
    order.is_valid = False
    order.is_delivered = False
    order.status = order.STATUS_CHOICES[3][1]
    order.save()
    for item in order.orderitem_set.all():
        item.subtotal_calculation()
    return redirect('Rachid:rorders')

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def cancelled_order(request, order_id):
    order = get_object_or_404(M.Order, id=order_id)
    order.is_cancelled = True
    order.is_valid = False
    order.is_returned = False
    order.is_delivered = False
    order.status = order.STATUS_CHOICES[0][1]
    order.save()
    for item in order.orderitem_set.all():
        item.subtotal_calculation()
    return redirect('Rachid:rorders')

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def delivered_order(request, order_id):
    order = get_object_or_404(M.Order, id=order_id)
    order.is_delivered = True
    order.is_cancelled = False
    order.is_valid = False
    order.is_returned = False
    order.status = order.STATUS_CHOICES[2][1]
    order.delivered_at = timezone.now()
    order.save()
    for item in order.orderitem_set.all():
        item.subtotal_calculation()
    return redirect('Rachid:rorders')

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def Valid_Orders(request):
    orders = M.Order.objects.filter(status='Validated')
    context = {
        'title':'Orders',
        'orders':orders,
    }
    return render(request,'Rachid/rachid_interface.html', context) 

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def Cancelled_Orders(request):
    orders = M.Order.objects.filter(status='Cancelled')
    context = {
        'title':'Orders',
        'orders':orders,
    }
    return render(request,'Rachid/rachid_interface.html', context) 

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def Returned_Orders(request):
    orders = M.Order.objects.filter(status='Returned')
    context = {
        'title':'Orders',
        'orders':orders,
    }
    return render(request,'Rachid/rachid_interface.html', context) 

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def Delivered_Orders(request):
    orders = M.Order.objects.filter(status='Delivered')
    context = {
        'title':'Orders',
        'orders':orders,
    }
    return render(request,'Rachid/rachid_interface.html', context) 

