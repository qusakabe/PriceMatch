from django.db import models

class Shop(models.Model):
    name = models.CharField(max_length=100)
    number_products = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.URLField()
    weight = models.CharField(max_length=20)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,default=1)
