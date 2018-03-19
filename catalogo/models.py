# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
    #Validación para nombre de usuario
    username = self.cleaned_data['username']
    if User.objects.filter(username=username):
        raise forms.ValidationError('El nombre de usuario ya existe! Por favor intenta otro.')
    return username

def clean_email(self):
    #Validación para correo electronico
    email = self.cleaned_data['email']
    if User.objects.filter(email=email):
        raise forms.ValidationError('El correo electronico ya existe! Intenta otro por favor.')
    return email

def clean_password2(self):
    #Comprueba que password  y password2 sean iguales.
    password =  self.cleaned_data['password']
    password2 = self.cleaned_data['password2']
    if password != password2:
        raise forms.ValidationError('Las contraseñas no coinciden. Intentalo nuevamente')
    return password2


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

    def __unicode__(self):
        return self.name
