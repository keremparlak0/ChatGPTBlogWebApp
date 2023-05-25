from django.urls import path
from . import views

urlpatterns = [
    #path("login", views.login_request, name="login"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("settings", views.settings, name="settings"),
    path("passwordchange", views.change_password, name="passwordchange"),
    path("emailchange", views.change_email, name="emailchange"),
    path("usernamechange", views.change_username, name="usernamechange"),
    path("userremove", views.remove_user, name="userremove"),
]