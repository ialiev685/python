from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=30)


class Product(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    price = models.IntegerField()
