# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-18 21:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0035_auto_20180517_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='tools',
        ),
    ]
