from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions


def home(request):
    template = 'main/home.html'
    return render(request, template)

