from django import forms
from .models import Client
class ClientForm(forms.ModelForm):
    
    class Meta:
        model = Client
        fields = ["full_name","phone","city",]
        labels = {
            'full_name' : 'الاسم الكامل',
            'phone' : 'الهاتف',
            'city' : 'المدينة',
        }
        
        widgets = {
            'full_name' : forms.TextInput(attrs={'class':'form-control'}),
            'phone' : forms.TextInput(attrs={'class':'form-control'}),
            'city' : forms.TextInput(attrs={'class':'form-control'}),
        }
