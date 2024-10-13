from django.db import models
from client.models import Client
from django.utils import timezone
from product.models import Product
# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ('cancelled', 'Cancelled'),
        ('validated', 'Validated'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
        ('dending', 'Pending'),
        # Add other statuses as necessary
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[4][1])
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    is_cancelled = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    delivered_at = models.DateTimeField(auto_now_add=True, null=True)
    products = models.ManyToManyField("product.Product", through='OrderItem')
    class Meta:
        verbose_name = ("Order")
        verbose_name_plural = ("Orders")
    
    def fix_status(self):
        if  self.is_delivered:
            self.status = self.STATUS_CHOICES[2][1]
            self.save()
        elif  self.is_cancelled : 
            self.status = self.STATUS_CHOICES[0][1]
            self.save()
        elif  self.is_returned:
            self.status = self.STATUS_CHOICES[3][1]
            self.save()
        elif  self.is_valid:
            self.status = self.STATUS_CHOICES[1][1]
            self.save()
        else:
            self.status = self.STATUS_CHOICES[4][1]
            self.save()
        return self
    def __str__(self):
        return f'order of user: {self.user.first_name}'
    def filling_thegap(self):
        if not self.created_at:
            self.created_at = timezone.now()
            self.save()
        if not self.is_delivered and not self.delivered_at :
            self.delivered_at = None
            self.save()
        return self

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    subtotal = models.IntegerField(default=0)
    class Meta:
        verbose_name = ("OrderItem")
        verbose_name_plural = ("OrderItems")
    
    def __str__(self) -> str:
        return f'order item of : {self.order.id}'
    
    def subtotal_calculation(self):
            self.subtotal = self.quantity * self.product.promotion_price
            self.save()
