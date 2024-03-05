from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import time, date, datetime

from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


#####################################################










####################################################################################

class ImageField(models.ImageField):
    def value_to_string(self, obj): # obj is Model instance, in this case, obj is 'Class'
        return obj.avatar.url # not return self.url


#######################################################################################
class ShopCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='category/', blank=True)
    slug = models.SlugField(max_length=200,
                            unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='category/', blank=True)
    slug = models.SlugField(max_length=200,
                            unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name

    # Other fields and methods as needed...

    
class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuário', blank=True)
    shop_category = models.ForeignKey(ShopCategory, related_name='shops', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=500, verbose_name='Nome do restaurante')
    phone = models.CharField(max_length=500, verbose_name='Telefone do restaurante')
    address = models.CharField(max_length=500, verbose_name='Endereço da loja')
    logo = models.ImageField(upload_to='restaurant_logo/', blank=False, verbose_name='Logotipo do restaurante')
    Shop_license = models.FileField(upload_to='vendor/license', blank=True, verbose_name='Licenca do restaurante')
    barnner = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name 


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, related_name='products', on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.CharField(max_length=200)
    images = models.JSONField(default=list)  # Assuming images are stored as a list of strings (URLs)
    rating = models.IntegerField()  # Assuming rating is an integer field
    seller = models.ForeignKey(Shop, on_delete=models.CASCADE)
    description = models.TextField()
   

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title   
  





