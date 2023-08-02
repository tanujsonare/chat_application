from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("api/create_room/<str:uuid>/", views.create_room, name="create_room")
]