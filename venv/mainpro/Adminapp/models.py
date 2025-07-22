from django.db import models

# Create your models here.

class Login(models.Model):
    uname=models.CharField(max_length=100)   
    pswd=models.CharField(max_length=100)
    utype=models.CharField(max_length=10)
    

class Cattegory(models.Model):
    cname=models.CharField(max_length=100)

class Subcattegory(models.Model):
    cid=models.ForeignKey(Cattegory,on_delete=models.CASCADE)
    scname=models.CharField(max_length=100)      

class Admin_Products(models.Model):
    cid=models.ForeignKey(Cattegory,on_delete=models.CASCADE)
    pname=models.CharField(max_length=100)
    desc=models.CharField(max_length=100)
    img=models.FileField(upload_to='file')
    rate=models.CharField(max_length=10)
    qty_in_gm=models.CharField(max_length=10)