from django.contrib.auth.views import LoginView
from django.urls import path

from .forms import LoginForm
from . import views

app_name = 'account'


urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html', form_class=LoginForm), name='login'),
    path('logout', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
]
