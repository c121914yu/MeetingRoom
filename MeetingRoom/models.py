from django.db import models

class user(models.Model):
    ID = models.CharField(max_length=100,primary_key=True, default='', editable=False)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=60)

class manager(models.Model):
    ID = models.CharField(max_length=100,primary_key=True, default='', editable=False)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=60)
    encode = models.TextField(default='')

class room(models.Model):
    ID = models.CharField(max_length=100,primary_key=True, default='', editable=False)
    place = models.CharField(max_length=60)
    maxPeople = models.IntegerField()
    introduction = models.CharField(max_length=255)
    condition = models.IntegerField(default=0)
    reserveInfo = models.TextField(default='')

class reserve(models.Model):
    ID = models.CharField(max_length=100,primary_key=True, default='', editable=False)
    condition = models.IntegerField(default=0)
    roomInfo = models.TextField(default='')
    reserveInfo = models.TextField(default='')
