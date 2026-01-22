from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("activate/<uidb64>/<token>/", views.activate_account, name="activate_account"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
]
