from django.urls import path

from inventory.views import InventoryList, InventoryRetrieve, UseUserItem, StatusList

urlpatterns = [
    path('inventory/<int:user_id>', InventoryList.as_view()),
    path('inventory/<int:user_id>/<int:item_id>', InventoryRetrieve.as_view(), name="get-inventory"),
    path('inventory/use/<int:user_id>/<int:item_id>', UseUserItem.as_view(), name="post-inventory"),
    path('status/<int:user_id>', StatusList.as_view())

]
"""path('inventory/add', CreateUserItem.as_view()),
path('inventory/use', UseUserItem.as_view())"""
