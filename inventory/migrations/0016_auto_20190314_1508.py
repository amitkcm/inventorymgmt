# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-14 15:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_userrole_role'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userrole',
            old_name='role',
            new_name='users',
        ),
    ]