from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("api/create_room/<str:uuid>/", views.create_room, name="create_room"),
    path("chat", views.chat, name="create_room"),
    path("admin-dashboard", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/room_details/<str:uuid>/", views.get_room_details, name="room_details"),
    path("admin-dashboard/add_user/", views.add_new_admin_user, name="add_new_admin_user"),
    path("admin-dashboard/user_details/<uuid:uuid>/", views.user_details, name="user_details"),
]