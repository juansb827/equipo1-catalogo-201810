# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-17 21:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0028_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='email',
            field=models.CharField(default='conectate@uniandes.edu.co', max_length=150),
            preserve_default=False,
        ),
    ]
