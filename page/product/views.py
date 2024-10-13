from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, ReviewForm, ReplyForm, RatingForm, ProductImageForm
from .models import Product, Review, Reply, ProductImage
from django.contrib.auth.decorators import user_passes_test, login_required

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        image_form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            product.instok()
            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image=image)
            return redirect('product:product_list')
        else:
            return render(request, 'product/add_product.html', {'form': form})
    else:
        form = ProductForm()
        image_form = ProductImageForm()
        return render(request, 'product/add_product.html', {'form': form, 'image_form':image_form,})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect('product:product_list')
    return render(request, 'product/delete_product.html', {'product': product})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        image_form = ProductImageForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            images = request.FILES.getlist('images')
            product_images = ProductImage.objects.filter(product=product)
            if len(product_images) == len(images):
                combo = zip(product_images, images)
                for product_image, image in combo:
                    product_image.image=image
                    product_image.save()
            elif len(product_images) < len(images):
                for image in images[len(product_images):]:
                    ProductImage.objects.get_or_create(product=product, image=image)
            return redirect('product:product_list')
    else:
        form = ProductForm(instance=product)
        image_form = ProductImageForm(instance=product)
    return render(request, 'product/edit_product.html', {'form': form, 'image_form':image_form,})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
@login_required
def product_list(request):
    products = Product.objects.all()
    for p in products:
        p.instok()
    return render(request, 'product/product_list.html', {'products': products})

def add_review(request, product_id):
    product = get_object_or_404(Product,id=product_id)
    if request.method == 'POST':
        rating = int(request.POST['rating'])
        review = ReviewForm(request.POST)

        if review.is_valid() and isinstance(rating, int):
            review_instence = Review.objects.create(product=product)
            review_instence.rating=rating
            review_instence.user=review.cleaned_data['user']
            review_instence.comment=review.cleaned_data['comment']
            review_instence.save()
            
    return redirect('core:home')

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
@login_required
def product_review_options(request):
    products = Product.objects.all()
    return render(request, 'product/review_manipulation.html', {'products':products})

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
@login_required
def toggle_visibility_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.is_active = not review.is_active
    review.save()
    return redirect('product:review_manipulation')

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
@login_required
def edit_review(request, review_id):
    
    review = get_object_or_404(Review, id=review_id)
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES, instance=review)
        rating_form = RatingForm(request.POST)
        if form.is_valid() and rating_form.is_valid() :
            review_instence = form.save()
            review_instence.rating = rating_form.cleaned_data['rating']
            
            review_instence.save()
            return redirect('product:review_manipulation')
        else:
            return render(request, 'product/edit_review.html', {'form': form, 'rating_form':rating_form })
    else:
        form = ReviewForm(instance=review)
        rating_form = RatingForm()
    return render(request, 'product/edit_review.html', {'form': form, 'rating_form':rating_form })

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
@login_required
def toggle_visibility_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    reply.is_active = not reply.is_active
    reply.save()

    return redirect('product:review_manipulation')

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
@login_required
def add_reply(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.review = review
            reply.save()
            return redirect('product:review_manipulation')
    else:
        form = ReplyForm()
    
    return render(request, 'product/reply_form.html', {'form': form, 'review': review, 'review_id':review_id })

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/login/')
@login_required
def edit_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    if request.method == "POST":
        form = ReplyForm(request.POST, request.FILES, instance=reply)
        if form.is_valid():
            form.save()
            return redirect('product:review_manipulation')
        else:
            print(form.errors)
            return render(request, 'product/edit_reply.html', {'form': form})
    else:
        form = ReplyForm(instance=reply)
        return render(request, 'product/edit_reply.html', {'form': form})