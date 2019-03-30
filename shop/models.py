from django.db import models

# Create your models here.


class Product(models.Model):
    icon = models.ImageField(upload_to='media/products/',default='aa',blank=True)
    firebase_id_token = models.CharField(max_length=50)