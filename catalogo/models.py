# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Tool(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    url = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class Example(models.Model):
    name = models.CharField(max_length=150)
    tool = models.ForeignKey(Tool, null=False)
    technology = models.ForeignKey(Technology, null=False)
