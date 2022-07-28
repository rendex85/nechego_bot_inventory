from django.urls import path

from inventory.views import  InventoryList, InventoryRetrieve

urlpatterns = [
    path('inventory/<int:user_id>', InventoryList.as_view()),
    path('inventory/<int:user_id>/<int:item_id>', InventoryRetrieve.as_view())


]
"""path('inventory/add', CreateUserItem.as_view()),
path('inventory/use', UseUserItem.as_view())"""