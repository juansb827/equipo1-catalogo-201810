# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-21 01:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0020_auto_20180420_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='integration',
            field=models.BooleanField(default=False),
        ),
    ]