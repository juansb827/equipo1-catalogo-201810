# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cloudinary.models import CloudinaryField
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm


# Create your models here.


class UserForm(ModelForm):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2']


def clean_username(self):
    # Validación para nombre de usuario
    username = self.cleaned_data['username']
    if User.objects.filter(username=username):
        raise forms.ValidationError('El nombre de usuario ya existe! Por favor intenta otro.')
    return username


def clean_email(self):
    # Validación para correo electronico
    email = self.cleaned_data['email']
    if User.objects.filter(email=email):
        raise forms.ValidationError('El correo electronico ya existe! Intenta otro por favor.')
    return email


def clean_password2(self):
    # Comprueba que password  y password2 sean iguales.
    password = self.cleaned_data['password']
    password2 = self.cleaned_data['password2']
    if password != password2:
        raise forms.ValidationError('Las contraseñas no coinciden. Intentalo nuevamente')
    return password2


class Technology(models.Model):
    name = models.CharField(max_length=150)
    thumbnail = CloudinaryField('image', null=True)  # Imagen que se ve en los resultados de busqueda
    description = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class Tool(models.Model):
    name = models.CharField(max_length=150)
    thumbnail = CloudinaryField('image', null=True)  # Imagen que se ve en los resultados de busqueda
    description = models.CharField(max_length=500)
    url = models.CharField(max_length=1000)
    technology = models.ForeignKey(Technology, null=True, blank=True)
    license_type = models.CharField(max_length=150)
    integration = models.BooleanField(default= False)
    use_restrictions = models.CharField(max_length=500, null=True)
    download_url = models.CharField(max_length=1000, null=True)
    functional_description = models.CharField(max_length=1000, default='')
    operating_systems = models.CharField(max_length=150, default='')

    def __unicode__(self):
        return self.name


class Example(models.Model):
    name = models.CharField(max_length=150)
    url = models.CharField(max_length=1000)
    tool = models.ForeignKey(Tool, null=False)
    technology = models.ForeignKey(Technology, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Tutorial(models.Model):
    name = models.CharField(max_length=150)
    url = models.CharField(max_length=1000)
    tool = models.ForeignKey(Tool, null=False)


class Strategy(models.Model):
    name = models.CharField(max_length=300)


class DevelopmentTechnology(models.Model):
    name = models.CharField(max_length=50)
    image = CloudinaryField('image', null=True)

    def __unicode__(self):
        return self.name


class Development(models.Model):
    name = models.CharField(max_length=150)
    dev_technologies = models.ManyToManyField(DevelopmentTechnology)

    def __unicode__(self):
        return self.name


ITEM_TYPE_CHOICES = (
    ('1', 'TECHNOLOGY'),
    ('2', 'TOOL'),
    ('3', 'TUTORIAL'),
    ('4', 'EXAMPLE'),
    ('5', 'STRATEGY'),
    ('6', 'DEVELOPMENT')
)

TECHNOLOGY = "1"
TOOL = "2"
TUTORIAL = "3"
EXAMPLE = "4"
STRATEGY = "5"
DEVELOPMENT = "6"

ITEM_TYPE_STATUS = (
    ('1', 'IN REVIEW'),
    ('2', 'ACCEPTED'),
    ('3', 'REJECTED'),
    ('4', 'UNFINISHED')
)


class Image(models.Model):
    image = CloudinaryField('image', null=True)

    @property
    def full(self):
        return self.image.public_id


class Item(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=300)
    thumbnail = CloudinaryField('image', null=True)  # Imagen que se ve en los resultados de busqueda
    type = models.CharField(max_length=1, choices=ITEM_TYPE_CHOICES)
    technology = models.ForeignKey(Technology, null=True, blank=True)
    tool = models.ForeignKey(Tool, null=True, blank=True)
    tutorial = models.ForeignKey(Tutorial, null=True, blank=True)
    example = models.ForeignKey(Example, null=True, blank=True)
    strategy = models.ForeignKey(Strategy, null=True, blank=True)
    development = models.ForeignKey(Development, null=True, blank=True)
    item_code = models.IntegerField(default=-1)  # Relaciona diferentes versiones de un mismo item
    version = models.IntegerField(default=0)  # Version del item
    status = models.CharField(max_length=1, choices=ITEM_TYPE_STATUS)
    images = models.ManyToManyField(Image)

    def __unicode__(self):
        return self.name + "   " + ITEM_TYPE_CHOICES[int(self.type) - 1][1]
