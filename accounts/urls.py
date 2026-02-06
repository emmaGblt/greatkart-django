from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("activate/<uidb64>/<token>/", views.activate_account, name="activate_account"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("forgot-password/", views.forgot_password, name="forgot-password"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("reset-password/", views.reset_password, name="reset-password"),
    path(
        "reset-password-validate/<uidb64>/<token>/",
        views.reset_password_validate,
        name="reset-password-validate",
    ),
    path("orders/<uuid:order_reference>/", views.order_detail, name="order-detail"),
    path("orders/", views.orders, name="orders"),
    path("edit-profile/", views.edit_profile, name="edit-profile"),
    path("change-password/", views.change_password, name="change-password"),
]
