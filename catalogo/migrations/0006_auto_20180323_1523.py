# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-23 20:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0005_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='tipo',
            new_name='type',
        ),
    ]
