# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-21 17:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0022_auto_20180420_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='example',
            name='technology',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogo.Technology'),
        ),
    ]