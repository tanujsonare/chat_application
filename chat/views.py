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
        Room.objects.create(uuid=uuid, client=name, url=url)
        # return render(request, "chat/chat_page_for_customer.html")
        return JsonResponse({"message": "Room created successfully"})
    except :
        return JsonResponse({"error_message": "An error occured while creating room."})
    

def chat(request):
    return render(request, "chat/chat_page_for_customer.html")