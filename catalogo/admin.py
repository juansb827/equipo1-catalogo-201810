# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
import catalogo.models as models

admin.site.register(models.Tool)
admin.site.register(models.Technology)
admin.site.register(models.Example)