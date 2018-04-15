# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import os

import cloudinary.api
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from models import UserForm, Item, Example, Tutorial
import models as models
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)


def index(request):
    return render(request, 'index.html', {})


# def login(request):
#   return render(request, 'login.html', {})


def example(request):
    request.GET = request.GET.copy()
    request.GET['type'] = '1'
    request.GET['name'] = None
    response = search_item(request)
    techs = json.loads(response.content)
    request.GET = request.GET.copy()
    request.GET['type'] = '2'
    request.GET['name'] = None
    response = search_item(request)
    tools = json.loads(response.content)
    context = {'techs': techs, 'tools': tools}
    return render(request, 'example.html', context)

def tutorial(request):
    request.GET = request.GET.copy()
    request.GET['type'] = '1'
    request.GET['name'] = None
    response = search_item(request)
    techs = json.loads(response.content)
    request.GET = request.GET.copy()
    request.GET['type'] = '2'
    request.GET['name'] = None
    response = search_item(request)
    tools = json.loads(response.content)
    context = {'tools': tools}
    return render(request, 'tutorial.html',context)


def add_example(request):
    example = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        url = request.POST.get('url')
        tool = request.POST.get('tool')
        tech = request.POST.get('tech')
        example = Example(
            name=name,
            url=url,
            tool_id=tool,
            technology_id=tech)
        example.save()
    return HttpResponse(serializers.serialize("json", [example]))

def add_tutorial(request):
    tutorial = {}
    if request.method == 'POST':
        name = request.POST.get('nameTuto')
        url = request.POST.get('url')
        description = request.POST.get('description')
        tool = request.POST.get('tool')
        tutorial = Tutorial(
            name=name,
            url=url,
            description = description,
            tool_id = tool)
        tutorial.save()
    return HttpResponse(serializers.serialize("json", [tutorial]))



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
        'form': form
    }
    return render(request, 'registro.html', {})
    # return render(request, 'catalogo/registro.html')


@csrf_exempt
def search_item(request):


    name = request.GET['name'];
    type = request.GET['type']
    # type='1'

    if name is not None:
        name = name.strip()

    print('type', name, type)

    query = Item.objects.all()

    if name is not None and name != "":


        tech = Item.objects.filter(Q(type='1')).filter(name__icontains=name)


        # el nombre contiene name o el nombre de su tecnologia contiene name
        tools = query.filter(type='2').filter(
            Q(name__icontains=name) | Q(tool__technology__id__in=tech.values('technology')))

        # el nombre contiene name , el nombre de su herramienta contiene name, el nombre de su tecnologia contiene name
        tutoriales = query.filter(type='3').filter(
            Q(name__icontains=name) | Q(tutorial__tool__id__in=tools.values('tool')))

        # el nombre contiene name , el nombre de su herramienta contiene name, el nombre de su tecnologia contiene name
        examples = query.filter(type='4').filter(
            Q(name__icontains=name) | Q(example__tool__id__in=tools.values('tool')))

        strategies = query.filter(type='5').filter( Q(name__icontains=name))

        if type == '1':
            query = tech
        elif type == '2':
            query = tools
        elif type == '3':
            query = tutoriales
        elif type == '4':
            query = examples
        elif type == '5':
            query= strategies
        else:
            query = tech.union(tools).union(tutoriales).union(examples).union(strategies)

    else:
        #No escribio un criterio de busqueda pero selecciono un tipo de item
        if type != '-1':
            query = query.filter(type=type)



    return HttpResponse(serializers.serialize("json", query))


def login_view(request):
    if request.user.is_authenticated():
        return redirect(reverse('catalogo:index'))

    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('catalogo:index'))
        else:
            mensaje = 'Nombre de usuario o clave incorrecta.'

    return render(request, 'login.html', {'mensaje': mensaje})

def estrategia_view(request):
    return render(request, 'estrategia.html', {})






@csrf_exempt
def add_estrategia(request):




    name = request.POST['name'];
    description = request.POST['description']
    thumbnail = request.POST['thumbnail']
    images = request.POST.getlist('images[]')
    type = request.POST['type']

    """if type == models.TECHNOLOGY:
        
    elif type == models.TOOL:
        
    elif type == models.TUTORIAL:
        
    elif type == models.EXAMPLE:
      """


    if thumbnail == '' :
        thumbnail == None


    item = Item(
        name=name,
        description=description,
        thumbnail=thumbnail,
        type=type,
    )

    ob = None

    if type == models.TECHNOLOGY:  #TODO: agregar cosas especificas de cada tipo de item
        ob = models.Technology(
            name=name
        )
        ob.save()
        item.technology = ob
    elif type == models.TOOL:
        ob = models.Tool(
            name=name
        )
        ob.save()
        item.tool = ob
    elif type == models.TUTORIAL:
        url = request.POST.get('url')
        tool = request.POST.get('tool')

        ob = models.Tutorial(
            name=name,
            url=url,
            description=description,
            tool_id=tool
        )
        ob.save()
        item.tutorial = ob
    elif type == models.EXAMPLE:

        url = request.POST.get('url')
        tool = request.POST.get('tool')
        tech = request.POST.get('tech')

        ob = Example(
            name=name,
            url=url,
            tool_id=tool,
            technology_id=tech)
        ob.save()
        item.example = ob

    elif type == models.STRATEGY:
        ob = models.Strategy(
            name=name
        )
        ob.save()
        item.strategy = ob

    item.save()



    for image in images:
        models.Image(item=item, image=image).save()
        print("se guarda imagen")



    print name,description,thumbnail,images
    _ob=serializers.serialize("json", [ob])
    _item = serializers.serialize("json", [item])

    return JsonResponse({'mensaje' : 'ok','item': _item,'strategy': _ob})




def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('catalogo:index'))

def carac_herramienta_view(request):
    return render(request, 'carac_herramienta.html', {})