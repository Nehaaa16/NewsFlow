from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    profilePic = models.ImageField(upload_to='profilePic', default=None)
    user = models.OneToOneField(User, primary_key = True,on_delete=models.CASCADE)
    name = models.CharField(max_length =30, blank = True, null = True)
    about = models.TextField(max_length = 200, blank=True)
    DOB = models.DateField(null=True)

class SavePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    description = models.TextField()
    published_at = models.DateTimeField()
    url = models.URLField()

    def __str__(self):
        return self.title


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    subscription_expiry = models.DateTimeField(null=True)

