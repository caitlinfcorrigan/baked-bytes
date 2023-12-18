from django import forms
from django.forms import ModelForm
from .models import Order_Detail

class OrderQuantityForm(forms.Form):
    quantity = forms.IntegerField(label="New Quantity", min_value=1)
    class Meta:
        model = Order_Detail