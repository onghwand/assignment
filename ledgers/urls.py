from django.urls import path
from . import views

urlpatterns = [
    path("<int:user_pk>/", views.ledger_list_or_create),
    path("<int:user_pk>/<int:ledger_pk>/", views.ledger_read_or_update_or_delete), 
    path("<int:user_pk>/<int:ledger_pk>/duplicate/", views.ledger_duplicate),
    path("<int:user_pk>/<int:ledger_pk>/url/", views.ledger_url),
]