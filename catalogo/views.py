# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from models import UserForm, Tool

# Create your views here.
from django.urls import reverse
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
  cloud_name = os.environ.get('CLOUDINARY_NAME'),
  api_key = os.environ.get('CLOUDINARY_API_KEY'),
  api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

def index(request):
    return render(request, 'index.html', {})


#def login(request):
#   return render(request, 'login.html', {})


def add_example(request):
    return render(request, 'add_example.html', {})

def add_user_view(request):
    if request.method == 'POST':
        form = UserForm(request.Post)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            password = cleaned_data.get('password')
            email = cleaned_data.get('email')

            user_model = User.objects.create_user(username=username, password=password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = email
            user_model.save()

            return HttpResponseRedirect(reverse('catalogo:index'))
    else:
        form = UserForm()
    context = {
        'form':form
    }
    return render(request, 'registro.html', {})
    #return render(request, 'catalogo/registro.html')

@csrf_exempt
def search_item(request):
    if request.user.is_authenticated():
        lista_imagenes=Tool.objects.all()
    else:
        lista_imagenes = Tool.objects.all()
    return HttpResponse(serializers.serialize("json", lista_imagenes))


def login_view(request):
    if request.user.is_authenticated():
        return redirect(reverse('catalogo:index'))

    mensaje = ''
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('catalogo:index'))
        else:
            mensaje = 'Nombre de usuario o clave incorrecta.'

    return render(request, 'login.html', {'mensaje':mensaje})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('catalogo:index'))