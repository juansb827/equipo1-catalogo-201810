# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-12 21:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0013_auto_20180412_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_code',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='item',
            name='version',
            field=models.IntegerField(default=0),
        ),
    ]
