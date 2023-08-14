from django.urls import path

from . import views

app_name = 'core'


urlpatterns = [
    path('home', views.index, name='index'),
    path('', views.home_not_authenticated, name="home_not_authenticated"),
    path('about/', views.about, name='about'),
]
