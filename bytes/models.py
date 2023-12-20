from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

# Profile model for storing the user's contact info
class Profile(models.Model):
    # Users do not get deleted - only set to inactive
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    add1 = models.CharField(max_length = 200)
    add2 = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    # Should state use a tuple to set choices?
    state = models.CharField(max_length = 2)
    zip = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.add1}, {self.add2}, {self.city}, {self.state} {self.zip}'
    

class Byte(models.Model):
    item = models.CharField(max_length=200)
    description = models.TextField(max_length=250)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    available = models.BooleanField(default = True)

    def __str__(self):
        return f'{self.item}'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'byte_id': self.id})
    
class Order(models.Model):
    # Prevent profile deletion if the user has orders
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now=True)
    purchased = models.BooleanField(default= False)

    def __str__(self):
        return f'{self.id} , {self.order_date}'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'order_id': self.id})

    class Meta:
        ordering = ['-order_date']

class Order_Detail(models.Model):
    # Order details is an indirect m:m between order & byte
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    byte = models.ForeignKey(Byte, on_delete=models.PROTECT)
    quantity = models.IntegerField()

    def __str__(self):
        return f'#{self.order} - Item: {self.byte}'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'order_detail_id': self.id})