from django.shortcuts import render, redirect
from product.models import Product, Review
from product.forms import ReviewForm
from django.db.models import Avg
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    # Fetch all products
    if 'has_visited' not in request.session:
        request.session['has_visited'] = True
    products = Product.objects.all()
    review_form = ReviewForm()
    for product in products:
        product.average_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg'] or 0
        product.get_averge_rating()
    title_ofc = "المنتوجات"
    return render(request, 'product/product_view.html', {'products': products,  'review_form':review_form, 'title_ofc':title_ofc,})

def success(request):
    redirect_url = request.GET.get('redirect_url', '')
    return render(request, 'core/success.html', {'redirect_url': redirect_url})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
@login_required
def dashboard(request):
    return render(request, 'core/Rachid_base.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('Rachid:rhome')  # Admin view
            elif user.is_staff:
                return redirect('Rachid:rhome')  # Staff view
            else:
                return redirect('/')  # Regular user
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    return render(request, 'core/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('core:login')

# Admin Dashboard View
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def admin_dashboard(request):
    return redirect('Rachid:rhome')

# Staff Dashboard View
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
def staff_dashboard(request):
    return redirect('Rachid:rhome')
