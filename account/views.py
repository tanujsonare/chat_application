from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from .forms import AddUserForm
from .models import User


# Create your views here.

def logout_view(request):
    logout(request)
    messages.info(request, "Logout successfully..")
    return redirect('/')


def register(request):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.set_password(request.POST.get('password'))
            user.save()
            messages.success(request, "You are register successfully.")
            return redirect('/login')
    else:
        form = AddUserForm()
    return render(request, "account/register.html", {"form": form})
