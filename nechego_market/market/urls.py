from django.urls import path

from market.views import ItemInGroupListView, CreateUserItem

urlpatterns = [
    path('market/<int:group_id>', ItemInGroupListView.as_view()),
    path('market/<int:group_id>/<int:item_id>', CreateUserItem.as_view()),
    ]