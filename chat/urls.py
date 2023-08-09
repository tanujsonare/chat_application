from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("api/create_room/<str:uuid>/", views.create_room, name="create_room"),
    path("chat", views.chat, name="create_room"),
    path("admin-dashboard", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/room_details/<str:uuid>/", views.get_room_details, name="room_details"),
]