# models.py
from django.db import models
from django.contrib.auth.hashers import make_password

class Reg(models.Model):

    LOCATION_CHOICES = [
        ('Thiruvananthapuram', 'Thiruvananthapuram'),
        ('Kollam', 'Kollam'),
        ('Pathanamthitta', 'Pathanamthitta'),
        ('Alappuzha', 'Alappuzha'),
        ('Kottayam', 'Kottayam'),
        ('Idukki', 'Idukki'),
        ('Ernakulam', 'Ernakulam'),  
    ]

    fname = models.CharField(max_length=100)
    sname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, null=True)  # Add this field
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    status = models.CharField(max_length=20, default='pending')  # pending/approved/rejected
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fname} {self.sname} ({self.username})"
    
class User_Products(models.Model):
    uid=models.ForeignKey('Userapp.Reg',on_delete=models.CASCADE)
    cid=models.ForeignKey('Adminapp.Cattegory',on_delete=models.CASCADE)
    scid=models.ForeignKey('Adminapp.Subcattegory',on_delete=models.CASCADE)
    qty_in_kg=models.IntegerField()
    img=models.FileField(upload_to='file')
    status=models.CharField(max_length=10)    
    date=models.DateField()