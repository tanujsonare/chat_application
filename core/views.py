from django.shortcuts import render


def index(request):
    return render(request, 'core/index.html')


def about(request):
    return render(request, 'core/about.html')


def home_not_authenticated(request):
    return render(request, "core/home_not_authenticated.html")