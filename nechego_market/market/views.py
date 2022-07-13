from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from market.models import Item
from market.serializer import ItemBaseSerializer


class ItemListView(generics.ListAPIView):
    """
    View для получения и отправки комментариев
    Комментарии можно получить или отправить, указав в адресе id экспертизы,
    При желании можно в параметрах указать блок комментариев для GET-запроса
    """
    queryset = Item.objects.all()
    serializer_class = ItemBaseSerializer


