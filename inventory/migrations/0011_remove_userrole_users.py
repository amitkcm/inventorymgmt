# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-13 20:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_userrole_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrole',
            name='users',
        ),
    ]