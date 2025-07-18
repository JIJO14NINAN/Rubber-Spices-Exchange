from django.db import models

# Create your models here.

class factory(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    license = models.FileField(upload_to='licenses/', blank=True, null=True)
    type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
