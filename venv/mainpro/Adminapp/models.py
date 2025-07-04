from django.db import models

# Create your models here.

class Reg(models.Model):
    name=models.CharField(max_length=100)
    gender=models.CharField(max_length=10)
    email=models.EmailField(max_length=100)
    pho=models.CharField(max_length=10)
    addr=models.CharField(max_length=100)
    loc=models.CharField(max_length=100)
    status=models.CharField(max_length=10)
    uname=models.CharField(max_length=100,default="")

class Login(models.Model):
    uname=models.CharField(max_length=100)   
    pswd=models.CharField(max_length=100)
    utype=models.CharField(max_length=10)
    uid=models.ForeignKey(Reg,on_delete=models.CASCADE) 
    

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

class Cart(models.Model):
    uid=models.ForeignKey(Reg,on_delete=models.CASCADE)
    pid=models.ForeignKey(Admin_Products,on_delete=models.CASCADE)
    no_of_items=models.IntegerField(max_length=10)
    total=models.IntegerField(max_length=10)

