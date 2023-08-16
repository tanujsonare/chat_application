import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.models import Group

from .models import Room
from account.models import User
from account.forms import AddAdminUserForm, EditUserForm


@require_POST
def create_room(request, uuid):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')
    try:
        Room.objects.create(uuid=uuid, client=name, url=url)
        return JsonResponse({"message": "Room created successfully"})
    except :
        return JsonResponse({"error_message": "An error occured while creating room."})
    

def chat(request):
    return render(request, "chat/chat_page_for_customer.html")


@login_required
def admin_dashboard(request):
    try:
        if request.user.groups.first().name == "Manager": 
            rooms = Room.objects.all()
            staff_users = User.objects.filter(is_staff=True)

            return render(request, "chat/admin_dashboard.html",{
                "rooms": rooms,
                "staff_users": staff_users
            })
        elif request.user.groups.first().name == "agent":
            rooms = Room.objects.all()
            return render(request, "chat/admin_dashboard.html",{
                "rooms": rooms
            })
    except:
        raise PermissionDenied


@login_required
def get_room_details(request, uuid):
    try:
        room = Room.objects.get(uuid=uuid)
        if room.agent == request.user or request.user.groups.first().name == "Manager" or (request.user.groups.first().name == "agent" and not room.agent):
            if request.user.groups.first().name == "agent" and room.status == Room.WAITING:
                room.status = Room.ACTIVE
                room.agent = request.user
                room.save()
                messages.info(request, f"{request.user.name} you are assigned as a agent for this chat room !!!!")
            return render(request, "chat/room_details.html", {"room": room})
        return render(request, "chat/room_details.html")
    except:
        return render(request, "chat/room_details.html")
    

def add_new_admin_user(request):
    try:
        if request.user.groups.first().name == "Manager":
            if request.method == "POST":               
                form = AddAdminUserForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.is_staff = True
                    user.set_password(request.POST.get("password"))
                    user.save()
                    if user.role == User.MANAGER: 
                        group = Group.objects.get(name='Manager')
                        group.user_set.add(user)
                    elif user.role == User.AGENT: 
                        group = Group.objects.get(name='agent')
                        group.user_set.add(user)
                    messages.success(request, "Requested user added successfully.")
                    return redirect("/admin-dashboard")
            else:
                form = AddAdminUserForm()
            return render(request, "chat/add_new_admin_user.html", {"form": form})
        else:
            messages.error(request, "You don't have permission to add new users !!!!")
            return redirect("/admin-dashboard")
    except:
        messages.error(request, "You don't have permission to add new users !!!!")
        return redirect("/admin-dashboard")
    

def user_details(request, uuid):
    if request.user.groups.first().name == "Manager":
        user = get_object_or_404(User, pk=uuid)
        rooms = user.rooms.all()
        return render(request, "chat/user_details.html",{
            "user": user,
            "rooms": rooms if rooms else None
        })
    else:
        raise PermissionDenied
    

def edit_staff_user(request, uuid):
    try:
        if request.user.groups.first().name == "Manager":
            user = get_object_or_404(User, pk=uuid)
            if request.method == "POST":
                form = EditUserForm(request.POST, instance=user)
                
                if form.is_valid():
                    form.save()
                    messages.success(request, f"{user.name} user profile updated successfully.")
                    return redirect("/admin-dashboard")
            else:
                form = EditUserForm(instance=user)
            return render(request, "chat/edit_staff_user_profile.html",{
                "form": form,
                "user": user
            })
        else:
            messages.error(request, "You don't have permission to add new users !!!!")
            return redirect("/admin-dashboard")
    except:
        messages.error(request, "You don't have permission to add new users !!!!")
        return redirect("/admin-dashboard")
    

def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if room:
        if room.agent == request.user or request.user.groups.first().name == "Manager":
            room.delete()
            messages.success(request, f'Requested chat room deleted successfully.')
            return redirect("/admin-dashboard")
        else:
            messages.error(request, "You don't have permission to add new users !!!!")
            return redirect("/admin-dashboard")
    messages.error(request, "Room does not exist !!!!")
    return redirect("/admin-dashboard")