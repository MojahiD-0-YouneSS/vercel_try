from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Sum, Count
from client.models import Client
# Create your models here.

class Product(models.Model):

    name = models.CharField(max_length=50)
    promotion_price = models.IntegerField(default=1)
    description = models.TextField(default='description !!')
    original_price = models.IntegerField(default=1)
    in_stock = models.BooleanField(default=False)
    quantity = models.IntegerField()
    average_rating = models.IntegerField(default=0)
    
    total_ratings = models.IntegerField(default=0)
    total_ratings_instences = models.IntegerField(default=0)
    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def __str__(self):
        return self.name
    def instok(self):
        if self.quantity != 0:
            self.in_stock = True
            self.save()
        return self
    def get_averge_rating(self):
        active_reviews = self.reviews.filter(is_active=True)
        aggregation = active_reviews.aggregate(
        total_ratings=Sum('rating'),
        average_rating=Avg('rating'),
        total_ratings_instances=Count('rating')
    )
        self.total_ratings = aggregation['total_ratings'] if aggregation['total_ratings'] else 0
        self.total_ratings_instances = aggregation['total_ratings_instances'] if aggregation['total_ratings_instances'] else 0
        self.average_rating = round(aggregation['average_rating'], 1) if aggregation['average_rating'] else 0
        self.save()
        return self

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Images/', null=True, blank=True)
    
    def __str__(self):
        return f"Image for {self.product.name}"
    
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.CharField(max_length=50)
    rating = models.IntegerField(default=1,)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    replies_data = models.ManyToManyField('Reply',  related_name='replies')
    def __str__(self):
        return f'{self.user} - {self.product.id} - {self.rating}'


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    reply_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    
    def __str__(self):
        return f'Review by {self.user.username} - {self.created_at}'
