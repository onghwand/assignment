from django.urls import path
from . import views

app_name = "ledgers"

urlpatterns = [
    path("<int:user_pk>/", views.ledger_list_or_create, name="list_or_create"),
    path("<int:ledger_pk>/detail/", views.ledger_read_or_update_or_delete, name="read_or_update_or_delete"), 
    path("<int:ledger_pk>/duplicate/", views.ledger_duplicate, name="duplicate"),
    path("<int:ledger_pk>/url/", views.make_shorten_url, name="shorten_url"),
]