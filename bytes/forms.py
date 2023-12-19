from django import forms
from django.forms import ModelForm
from .models import Order, Order_Detail

class OrderQuantityForm(forms.Form):
    quantity = forms.IntegerField(label="New Quantity", min_value=1)
    class Meta:
        model = Order_Detail

class CheckoutForm(forms.Form):
    purchased = forms.BooleanField()
    class Meta:
        model = Order