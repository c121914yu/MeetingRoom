from django.db import models
 
class user(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=60)
    ID = models.CharField(max_length=100,primary_key=True,unique=True,default='')

class manager(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=60)
    ID = models.CharField(max_length=100,primary_key=True,unique=True,default='')
    encode = models.TextField(default='')