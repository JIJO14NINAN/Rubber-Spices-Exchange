from django.db import models
from Userapp.models import User_Products
# Create your models here.

class Staff(models.Model):
    name=models.CharField(max_length=100)
    gender=models.CharField(max_length=10)
    pho=models.IntegerField()
    email=models.EmailField(max_length=100)
    photo=models.FileField(upload_to='file')
    addr=models.CharField(max_length=100)

class ProductAssignment(models.Model):
    product = models.ForeignKey(User_Products, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)