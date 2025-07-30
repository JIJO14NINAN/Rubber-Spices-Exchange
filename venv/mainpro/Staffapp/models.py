from django.db import models
from Userapp.models import User_Products

class Staff(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    pho = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    photo = models.FileField(upload_to='photos/')  # Ensure this path is correct
    addr = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class ProductAssignment(models.Model):
    product = models.ForeignKey(User_Products, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)