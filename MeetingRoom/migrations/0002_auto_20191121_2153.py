# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-11-21 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MeetingRoom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='ID',
            field=models.CharField(default='', editable=False, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='room',
            name='ID',
            field=models.CharField(default='', editable=False, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='ID',
            field=models.CharField(default='', editable=False, max_length=100, primary_key=True, serialize=False),
        ),
    ]