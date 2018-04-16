# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from encodings.punycode import adapt

from django.contrib import admin

# Register your models here.
import catalogo.models as models

admin.site.register(models.Item)
admin.site.register(models.Technology)
admin.site.register(models.Tool)
admin.site.register(models.Tutorial)
admin.site.register(models.Example)
admin.site.register(models.Strategy)
admin.site.register(models.Image)
admin.site.register(models.DevelopmentTechnology)