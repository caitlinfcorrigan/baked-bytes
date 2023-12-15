from django.contrib import admin
from .models import Profile, Byte, Order, Order_Detail

# Register your models here.
admin.site.register(Profile)
admin.site.register(Byte)
admin.site.register(Order)
admin.site.register(Order_Detail)