from django.db import models

# Create your models here.
class MyUser(models.Model):
    email = models.CharField(max_length=10, unique=True, null=False)
    passwod = models.CharField(max_length=10, null=False)