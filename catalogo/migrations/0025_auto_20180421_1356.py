# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-21 18:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0024_auto_20180421_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorial',
            name='description',
        ),
        migrations.RemoveField(
            model_name='tutorial',
            name='thumbnail',
        ),
    ]
