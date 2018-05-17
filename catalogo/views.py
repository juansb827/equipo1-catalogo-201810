# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import os

# import cloudinary.api
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, Prefetch
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.utils.encoding import smart_text
from django.views.decorators.csrf import csrf_exempt

from models import UserForm, Item, Example, Tutorial, Tool
import models as models

CLOUDINARY_NAME = os.environ.get('CLOUDINARY_URL').split('@')[1]
print("NAME", CLOUDINARY_NAME)


def index(request):
    return render(request, 'index.html', {'CLOUDINARY_NAME': CLOUDINARY_NAME})


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
    return render(request, 'tutorial.html', context)


def tool(request):
    return render(request, 'herramienta.html')


def add_tool(request):
    t = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        t = Tool(
            name=name)
        t.save()
    return HttpResponse(serializers.serialize("json", [t]))


def add_example(request):
    ex = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        url = request.POST.get('url')
        tool = request.POST.get('tool')
        tech = request.POST.get('tech')
        ex = Example(
            name=name,
            url=url,
            tool_id=tool,
            technology_id=tech)
        ex.save()
    return HttpResponse(serializers.serialize("json", [ex]))


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
            description=description,
            tool_id=tool)
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

    authenticated = request.user.is_authenticated()

    if name is not None:
        name = name.strip()

    print('type', name, type)

    query = Item.objects.all()
    if not authenticated: query = query.filter(version='2')

    if name is not None and name != "":

        tech = query.filter(Q(type='1')).filter(name__icontains=name)

        # el nombre contiene name o el nombre de su tecnologia contiene name
        tools = query.filter(type='2').filter(
            Q(name__icontains=name) | Q(tool__technology__id__in=tech.values('technology')))

        # el nombre contiene name , el nombre de su herramienta contiene name, el nombre de su tecnologia contiene name
        tutoriales = query.filter(type='3').filter(
            Q(name__icontains=name) | Q(tutorial__tool__id__in=tools.values('tool')))

        # el nombre contiene name , el nombre de su herramienta contiene name, el nombre de su tecnologia contiene name
        examples = query.filter(type='4').filter(
            Q(name__icontains=name) | Q(example__tool__id__in=tools.values('tool')))

        strategies = query.filter(type='5').filter(Q(name__icontains=name))

        developments = query.filter(type='6').filter(Q(name__icontains=name))

        if type == '1':
            query = tech
        elif type == '2':
            query = tools
        elif type == '3':
            query = tutoriales
        elif type == '4':
            query = examples
        elif type == '5':
            query = strategies
        elif type == '6':
            query = developments
        else:
            query = tech.union(tools).union(tutoriales).union(examples).union(strategies).union(developments)

    else:
        # No escribio un criterio de busqueda pero selecciono un tipo de item
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
    data = json.loads(request.body)
    name = data['name'];
    description = data['description']
    thumbnail = data['thumbnail']
    # getlist('images[]')
    images = data['images']
    type = data['type']
    author = data['author']

    if thumbnail == '':
        thumbnail == None

    itemCode = data['id']

    print 'add_estrategia', itemCode

    if itemCode == '' or itemCode == 0:
        item = Item()
        item.type = int(smart_text(type, encoding='utf-8', strings_only=False, errors='strict'))
    else:
        item = Item.objects.get(item_code=itemCode, version=0, author=author)

    item.name = smart_text(name, encoding='utf-8', strings_only=False, errors='strict')
    item.description = smart_text(description, encoding='utf-8', strings_only=False, errors='strict')
    item.thumbnail = thumbnail
    item.status = '1'
    item.author_id = author

    ob = None

    if type == models.TECHNOLOGY:  # TODO: agregar cosas especificas de cada tipo de item
        ob = models.Technology(
            name=name,
            description=':V',
            url=''
        )
        ob.save()
        item.technology = ob
    elif type == models.TOOL:
        devPk = data['subclassId'];
        print "toolPk", devPk

        if devPk == '':
            ob = models.Tool()
        else:
            ob = models.Development.objects.get(pk=devPk)

        ob.name = name
        ob.description = ':v'
        ob.technology = models.Technology.objects.get(pk=data['technology'])
        ob.url = data['toolUrl']
        ob.download_url = data['toolDownloadUrl']
        ob.license_type = data['licenseType']
        ob.use_restrictions = data['useRestrictions']
        ob.integration = data['integration']
        ob.functional_description = data['functionalDescription']
        ob.operating_systems = smart_text(",".join(data['operativeSystems']), encoding='utf-8', strings_only=False,
                                          errors='strict')

        ob.save()
        item.tool = ob

    elif type == models.TUTORIAL:
        devPk = data['subclassId'];
        print "tutorialPk", devPk

        if devPk == '':
            ob = models.Tutorial()
        else:
            ob = models.Tutorial.objects.get(pk=devPk)

        ob.name = name
        ob.url = data['tutorialUrl']
        ob.tool_id = data['tool']

        ob.save()
        item.tutorial = ob
    elif type == models.EXAMPLE:

        devPk = data['subclassId'];
        print "examplePk", devPk

        if devPk == '':
            ob = models.Example()
        else:
            ob = models.Example.objects.get(pk=devPk)

        ob.name = name
        ob.url = data['exampleUrl']
        ob.strategy_id = data['strategy']
        ob.tool_id = data['tool']

        ob.save()
        item.example = ob

    elif type == models.STRATEGY:

        devPk = data['subclassId'];
        print "strategyPk", devPk

        if devPk == '':
            ob = models.Strategy()
        else:
            ob = models.Strategy.objects.get(pk=devPk)

        ob.name = name
        ob.save()
        item.strategy = ob

    elif type == models.DEVELOPMENT:
        devPk = data['subclassId'];
        print "devPk", devPk
        if devPk == '':
            ob = models.Development(
                name=name
            )
            ob.save()
        else:
            ob = models.Development.objects.get(pk=devPk)
            ob.dev_technologies.clear()
            ob.save()

        for tech in data['devTechs']:  # the list of devTechs PK's
            print "tech", tech
            ob.dev_technologies.add(tech)

        ob.save()
        item.development = ob

    item.save()

    if item.item_code == -1:
        print "Version ", data['version']
        if data['version'] == "2":
            print "Created draft of an aproved item"
            item.item_code = data['item_code']
        else:
            item.item_code = item.pk
        item.save()

    item.images.clear()
    for image in images:
        newImg = models.Image.objects.create(image=image)
        item.images.add(newImg)

    item.save()

    print name, description, thumbnail, images
    _ob = serializers.serialize("json", [ob])
    _item = serializers.serialize("json", [item])

    sendToReview = data['sendToReview'];

    if (sendToReview):
        createReviewVersion(item)

    return JsonResponse({'mensaje': 'ok', 'item': _item, 'strategy': _ob})


""" Crea una copia del item """


def createReviewVersion(item):
    item.version = 1
    item.save()
    return

    print 'createReviewVersion', item.type

    # Si ya hay una version 'Review' del item la borra
    item_review = models.Item.objects.filter(item_code=item.item_code, version='1')
    if len(item_review) > 0:
        item_review[0].delete()

    # Crea una copia de la subclase del item
    if item.type == models.DEVELOPMENT:
        development = models.Development.objects.get(pk=item.development.pk)
        devTechs = development.dev_technologies.all()
        development.pk = None
        development.name = development.name + '+1'
        development.save()
        development.dev_technologies.set(devTechs)  # le asigna las mismas tecnologias a la copia
        development.save()
        item.development = development
    elif item.type == models.TOOL:
        tool = models.Tool.objects.get(pk=item.tool.pk)
        tool.pk = None
        tool.name = tool.name
        tool.save()
        item.tool = tool
    elif item.type == models.EXAMPLE:
        example = models.Example.objects.get(pk=item.example.pk)
        example.pk = None
        example.name = example.name
        example.save()
        item.example = example
    elif item.type == models.TUTORIAL:
        tutorial = models.Tutorial.objects.get(pk=item.tutorial.pk)
        tutorial.pk = None
        tutorial.name = tutorial.name
        tutorial.save()
        item.tutorial = tutorial
    elif item.type == models.STRATEGY:
        strategy = models.Strategy.objects.get(pk=item.strategy.pk)
        strategy.pk = None
        strategy.name = strategy.name
        strategy.save()
        item.strategy = strategy

    # Crea unacopia del item
    images = item.images.all()
    item.pk = None
    item.version = 1
    item.save()
    item.images.set(images)  # le asigna las mismas imagenes a la copia
    item.save()


""" Cambia el status del item a aprobado """


@csrf_exempt
def aprobarRevision(request):
    data = json.loads(request.body);

    item_code = data['item_code']
    version = data['version']
    approved = data['approved']
    author_id = data['author_id']

    item = models.Item.objects.get(item_code=item_code, version=1, author=author_id)
    if approved:
        # revisa si ya existe una version aprobada y la elimina
        aprobada = models.Item.objects.filter(item_code=item_code, version=2)
        if len(aprobada) != 0:
            aprobada[0].delete()

        item.version = 2
    else:  # La devuelve a borrador
        item.version = 0

    item.save()

    return JsonResponse({'mensaje': 'ok'})


def crear_tutorial_view(request):
    return createItemView(request, models.TUTORIAL)


def crear_ejemplo_view(request):
    return createItemView(request, models.EXAMPLE)


def crear_herramienta_view(request):
    return createItemView(request, models.TOOL)


def crear_estrategia_view(request):
    return createItemView(request, models.STRATEGY)


def crear_desarrollo_view(request):
    return createItemView(request, models.DEVELOPMENT)


def createItemView(request, type):
    return render(request, 'desarrollo.html', {
        'itemType': type,
        'itemId': '',
        'itemVer': '',
        'CLOUDINARY_NAME': CLOUDINARY_NAME
    })


def mostrar_item(request):
    print request.GET['type']
    print request.GET['code']
    print request.GET['ver']
    return render(request, 'desarrollo.html', {
        'itemType': request.GET['type'],
        'itemId': request.GET['code'],
        'itemVer': request.GET['ver'],
        'CLOUDINARY_NAME': CLOUDINARY_NAME
    })


def get_item(request):
    id = request.GET['id']
    type = request.GET['type']
    version = request.GET['version']
    print id, type, version
    item = models.Item.objects.filter(item_code=id, version=version, type=type)

    if len(item) == 0:
        print 'item not found'
        # return JsonResponse({'mensaje': 404})

    images = item[0].images.all()
    imgs_res = []
    for img in images:
        imgs_res.append({'id': img.pk, 'remoteId': img.full})

    res = {
        'images': json.dumps(imgs_res),
        'item': serializers.serialize("json", [item[0]])
    }

    if (type == models.DEVELOPMENT):  # TODO remove duplicated code
        techs = item[0].development.dev_technologies.all()
        res['techs'] = serializers.serialize("json", techs)
    elif (type == models.TOOL):
        subItem = models.Tool.objects.filter(pk=item[0].tool.pk)
        res['subItem'] = serializers.serialize("json", subItem)
    elif (type == models.EXAMPLE):
        subItem = models.Example.objects.filter(pk=item[0].example.pk)
        res['subItem'] = serializers.serialize("json", subItem)
    elif (type == models.TUTORIAL):
        subItem = models.Tutorial.objects.filter(pk=item[0].tutorial.pk)
        res['subItem'] = serializers.serialize("json", subItem)
    elif (type == models.STRATEGY):
        subItem = models.Strategy.objects.filter(pk=item[0].strategy.pk)
        res['subItem'] = serializers.serialize("json", subItem)

    return HttpResponse(json.dumps(res))


# TODO: unir los metodos en uno solo
def getMembers(request):
    members = models.Member.objects.all()
    context = {'members': members}
    return render(request, 'equipo.html', context)


def getDevTech(request):
    techs = models.DevelopmentTechnology.objects.all()
    return HttpResponse(serializers.serialize("json", techs))


def technologies(request):
    technologies = models.Technology.objects.all()
    return HttpResponse(serializers.serialize("json", technologies))


def tools(request):
    tools = models.Item.objects.filter(type=models.TOOL, version='2')
    return HttpResponse(serializers.serialize("json", list(tools), fields=('item_code', 'name', 'tool')))


def strategies(request):
    strategies = models.Item.objects.filter(type=models.STRATEGY, version='2')
    return HttpResponse(serializers.serialize("json", list(strategies), fields=('item_code', 'name', 'strategy')))
    # return HttpResponse(serializers.serialize("json", strategies))


def integrante_view(request):
    # testing commit againa again again!
    return render(request, 'integrante.html', {'member_id': 5})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('catalogo:index'))


def carac_herramienta_view(request):
    # testing commit againa again again!
    return render(request, 'carac_herramienta.html', {})
