from django.db import models
 
class user(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=60)