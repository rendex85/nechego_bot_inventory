from django.urls import path

from inventory.views import CreateUserItem, UseUserItem
from market.views import ItemListView

urlpatterns = [
    path('inventory/add', CreateUserItem.as_view()),
    path('inventory/use', UseUserItem.as_view())
    ]