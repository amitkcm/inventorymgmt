# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-10 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_auto_20190310_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='batch_date',
            field=models.DateField(),
        ),
    ]
