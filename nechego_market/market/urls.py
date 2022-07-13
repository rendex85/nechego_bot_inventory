from django.urls import path

from market.views import ItemListView

urlpatterns = [
    path('market', ItemListView.as_view()),
    ]