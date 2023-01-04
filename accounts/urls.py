from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("test/", views.test),
    path("signup/", views.signup),
    path("login/", views.login),
    path("logout/", views.logout),
]