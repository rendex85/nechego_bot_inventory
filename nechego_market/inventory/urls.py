from django.urls import path

from inventory.views import CreateUserItem, InventoryList

urlpatterns = [
    path('inventory/<int:user_id>', InventoryList.as_view()),


]
"""path('inventory/add', CreateUserItem.as_view()),
path('inventory/use', UseUserItem.as_view())"""