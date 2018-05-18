# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-17 18:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0027_item_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('tools', models.ManyToManyField(to='catalogo.Tool')),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(choices=[('1', 'TECHNOLOGY'), ('2', 'TOOL'), ('3', 'TUTORIAL'), ('4', 'EXAMPLE'), ('5', 'STRATEGY'), ('6', 'DEVELOPMENT'), ('7', 'DISCIPLINE')], max_length=1),
        ),
        migrations.AddField(
            model_name='item',
            name='discipline',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogo.Discipline'),
        ),
    ]