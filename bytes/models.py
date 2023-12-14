from django.db import models
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