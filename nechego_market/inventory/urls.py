from django.urls import path

from inventory.views import CreateUserItem
from market.views import ItemListView

urlpatterns = [
    path('inventory/add', CreateUserItem.as_view()),
    ]