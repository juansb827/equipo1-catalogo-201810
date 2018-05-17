# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-17 21:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0029_member_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='experience_years',
        ),
        migrations.AddField(
            model_name='member',
            name='experience_areas',
            field=models.CharField(default='Sicua', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
