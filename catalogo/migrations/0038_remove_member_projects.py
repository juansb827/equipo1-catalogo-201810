# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-18 21:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0037_member_tools'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='projects',
        ),
    ]
