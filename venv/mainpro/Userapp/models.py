from django.db import models
from django.contrib.auth.hashers import make_password

class Reg(models.Model):
    fname = models.CharField(max_length=100)
    sname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
class User_Products(models.Model):
    uid=models.ForeignKey('Userapp.Reg',on_delete=models.CASCADE)
    cid=models.ForeignKey('Adminapp.Cattegory',on_delete=models.CASCADE)
    scid=models.ForeignKey('Adminapp.Subcattegory',on_delete=models.CASCADE)
    qty_in_kg=models.IntegerField()
    img=models.FileField(upload_to='file')
    status=models.CharField(max_length=10)    
    date=models.DateField()