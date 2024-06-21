# my_app/forms.py

from django import forms
from .models import Product,OrderItem
from django.contrib.auth.models import User

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'base_price']

class ProductForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label="Select Product")
    quantity = forms.IntegerField(min_value=1, label="Quantity")

class OrderForm(forms.Form):
    product_forms = forms.formset_factory(ProductForm, extra=1)

class AddToOrderForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    product = forms.ModelChoiceField(queryset=Product.objects.all(), label="Select Product")
    quantity = forms.IntegerField(min_value=1, label="Quantity")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']


