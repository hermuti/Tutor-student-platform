from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.home_view, name="home"),
    path("user/", views.user_view, name="user"),
]



