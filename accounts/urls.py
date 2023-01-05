from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup),
    path("login/", views.login),
    path("logout/", views.logout),
    path("token/refresh/", TokenRefreshView.as_view()),
]