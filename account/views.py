from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages


# Create your views here.

def logout_view(request):
    logout(request)
    messages.info(request, "Logout successfully..")
    return redirect('/')
