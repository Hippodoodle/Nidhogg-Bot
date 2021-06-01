from django.shortcuts import render
from django.http import HttpResponse  # noqa: F401


def index(request):
    return render(request, 'bot/index.html')
