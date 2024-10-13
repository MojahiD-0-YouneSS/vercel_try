from django import forms
from .models import Product, Review, Reply, ProductImage

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ["name", "promotion_price", 'original_price',  "quantity",]
        labels = {
            'name': 'Name',
            'original_price': 'Original Price',
            'promotion_price':'Promotion Price',
            'quantity':'Quantity'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'original_price': forms.NumberInput(attrs={'class':'form-control'}),
            'promotion_price': forms.NumberInput(attrs={'class':'form-control'}),
            'quantity':forms.NumberInput(attrs={'class':'form-control'}),
        }
class RatingForm(forms.Form):
    rating = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={ 'class':'form-control'}))
    
    labels = {
        'rating':'Rating'
    }

class ProductImageForm(forms.ModelForm):
    images = forms.FileField(required=False, widget = forms.TextInput(attrs={
            "name": "images",
            "type": "File",
            "class": "form-control",
            "multiple": "True",
        }), label = "Images")
    class Meta: 
        model = ProductImage
        fields = ['image']
class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ['user', 'comment',]
        labels ={
            'user':' الاسم ',
            'comment':' التعليق ',
        }
        widgets = {
            'user': forms.TextInput(attrs={'class':'form-control'}),
            'comment': forms.Textarea(attrs={'class':'form-control', 'rows':8,}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_data', 'is_active']
        widgets = {
            'reply_data': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your reply here...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }