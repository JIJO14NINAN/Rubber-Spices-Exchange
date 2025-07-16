from django.db import models

# Create your models here.

class User_Products(models.Model):
    uid=models.ForeignKey('Adminapp.Reg',on_delete=models.CASCADE)
    cid=models.ForeignKey('Adminapp.Cattegory',on_delete=models.CASCADE)
    scid=models.ForeignKey('Adminapp.Subcattegory',on_delete=models.CASCADE)
    qty_in_kg=models.IntegerField()
    img=models.FileField(upload_to='file')
    status=models.CharField(max_length=10)    
    date=models.DateField()