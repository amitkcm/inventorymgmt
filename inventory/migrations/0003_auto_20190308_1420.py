# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-08 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20190308_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, null=True, unique=True, verbose_name='email address'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ManyToManyField(blank=True, null=True, to='inventory.UserRole'),
        ),
        migrations.AddField(
            model_name='user',
            name='staff',
            field=models.BooleanField(default=False),
        ),
    ]
