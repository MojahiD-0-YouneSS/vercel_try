from django.shortcuts import render, redirect
from .models import Client
from .forms import ClientForm
from django.urls import reverse

# Create your views here.

def client_info(request, product_id):
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            user = client_form.save()
            request.session['anonymos_user_id'] = user.id
            return redirect('orders:make_order', product_id=product_id,)
        else:
            context= {
            'client_form' : client_form,
            'product_id':product_id,
        }
            return render(request, 'client/client_info.html', context)
    else:
        client_form = ClientForm()
        context = {
            'client_form':client_form,
            'product_id':product_id,
        }
        return render(request, 'client/client_info.html', context)
