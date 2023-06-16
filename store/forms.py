from django import forms
from .models.contact import Contact
from django.contrib.auth.forms import PasswordResetForm
from .models.product import Products
from .models.orders import Order
from .models.customer import Customer


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['first_name','last_name','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
    
class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['first_name','last_name','phone']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}),
    )

class ProductForm(forms.ModelForm):
    class Meta:
        model=Products
        fields=['name','price','description','image','category','weight']


#for updating status of order
class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['status']

#address of shipment
class AddressForm(forms.Form):
    Email = forms.EmailField()
    Phone= forms.IntegerField()
    Address = forms.CharField(max_length=500)

