import json
from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST

from .models import Room


@require_POST
def create_room(request, uuid):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')
    try:
        Room.objects.create(uuid=uuid, name=name, url=url)
        return JsonResponse({"message": "Room created successfully."})
    except Exception as e:
        raise Exception(e)
    