# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-17 23:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0033_auto_20180517_1655'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExperienceArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
    ]