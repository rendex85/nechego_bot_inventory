from django.urls import path

from market.views import ItemListView

urlpatterns = [
    path('api/items/list', ItemListView.as_view()),
    ]