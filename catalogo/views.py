# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def login(request):
    return render(request, 'login.html', {})


def add_example(request):
    return render(request, 'add_example.html', {})
