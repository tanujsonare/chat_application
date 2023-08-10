import json
from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import Room
from account.models import User

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
        elif request.user.groups.first().name == "agents":
            rooms = Room.objects.all()
            return render(request, "chat/admin_dashboard.html",{
                "rooms": rooms
            })
    except:
        raise PermissionDenied


@login_required
def get_room_details(request, uuid):
    try:
        if request.user.groups.first().name == "Manager" or request.user.groups.first().name == "agents":
            room = Room.objects.get(uuid=uuid)
            if request.user.groups.first().name == "agents" and room.status == Room.WAITING:
                room.status = Room.ACTIVE
                room.agent = request.user
                room.save()
                messages.info(request, f"{request.user.name} you are assigned as a agent for this chat room !!!!")
            return render(request, "chat/room_details.html", {"room": room})
    except:
        raise PermissionDenied