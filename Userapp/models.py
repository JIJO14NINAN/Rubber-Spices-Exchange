from django.db import models

# Create your models here.

class Order_Master(models.Model):
    uid=models.ForeignKey('Adminapp.Reg',on_delete=models.CASCADE)
    order_date=models.DateField()
    gtotal=models.IntegerField()

class Order_Child(models.Model):
    order_id=models.ForeignKey(Order_Master,on_delete=models.CASCADE)
    pid=models.ForeignKey('Adminapp.Admin_Products',on_delete=models.CASCADE)
    no_of_items=models.IntegerField()
    total=models.IntegerField()
    status=models.CharField(max_length=10)

class User_Products(models.Model):
    uid=models.ForeignKey('Adminapp.Reg',on_delete=models.CASCADE)
    cid=models.ForeignKey('Adminapp.Cattegory',on_delete=models.CASCADE)
    scid=models.ForeignKey('Adminapp.Subcattegory',on_delete=models.CASCADE)
    qty_in_kg=models.IntegerField()
    img=models.FileField(upload_to='file')
    status=models.CharField(max_length=10)    
    date=models.DateField()