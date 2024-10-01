from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=20)


class Account(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True)
