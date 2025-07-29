from django.db import models

# Create your models here.  

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
    qty_in_kg=models.CharField(max_length=10)

class Stocks(models.Model):
    date=models.DateField(auto_now_add=True)
    pname=models.CharField(max_length=100)
    qty_in_kg=models.CharField(max_length=10)
    price=models.CharField(max_length=10)
    status=models.CharField(max_length=10,default='Available')
