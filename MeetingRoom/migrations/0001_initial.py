# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-11-21 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='manager',
            fields=[
                ('ID', models.CharField(default='', editable=False, max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=60)),
                ('encode', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='room',
            fields=[
                ('ID', models.CharField(default='', editable=False, max_length=50, primary_key=True, serialize=False)),
                ('place', models.CharField(max_length=60)),
                ('maxPeople', models.IntegerField()),
                ('introduction', models.CharField(max_length=255)),
                ('condition', models.IntegerField()),
                ('reserveInfo', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('ID', models.CharField(default='', editable=False, max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=60)),
            ],
        ),
    ]
