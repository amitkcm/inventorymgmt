# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-10 16:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_inventory_operation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ManyToManyField(blank=True, to='inventory.UserRole'),
        ),
    ]