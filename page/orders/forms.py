from django import forms
from .models import Order, OrderItem
class EditOrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['status', 'user', 'is_cancelled', 'is_delivered', 'is_valid', 'is_returned']
        
OrderItemFormSet = forms.inlineformset_factory(
    Order, 
    OrderItem, 
    fields=['product', 'quantity', 'subtotal'],
    extra=1,  
    can_delete=True,
)
