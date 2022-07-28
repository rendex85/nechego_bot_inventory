# Create your views here.
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response

from inventory.models import UserItem
from inventory.remove_add_item import inventory_change
from inventory.serializer import CreateUserItemSerializer, UseUserItemSerializer, UserItemSerializer
from market.models import Item
from market.serializer import ItemBaseSerializer, ItemInfoSerializer


class InventoryList(generics.ListAPIView):
    """
    Список предметов в инвентаре пользователя
    """
    queryset = UserItem.objects.all()
    serializer_class = UserItemSerializer

    def get_queryset(self):
        items_group = UserItem.objects.filter(user__uid=self.request.resolver_match.kwargs['user_id'], stock__gt=0)
        return items_group


class InventoryRetrieve(generics.RetrieveAPIView):
    """
    Конкретный предмет в инвентаре пользователя
    """
    queryset = UserItem.objects.all()
    serializer_class = ItemInfoSerializer

    def get_object(self):
        queryset = self.get_queryset()
        user = self.request.resolver_match.kwargs['user_id']
        item = self.request.resolver_match.kwargs['item_id']
        obj = get_object_or_404(queryset, user__id=user, item__id=item)
        return obj


class UseUserItem(generics.CreateAPIView):
    """
    Использование айтема
    поле stock в возвращаемых параметрах показывает актуальное количество предметов у пользователя
    """
    queryset = UserItem.objects.all()
    serializer_class = CreateUserItemSerializer
    # TODO: Сериализер
    @swagger_auto_schema(responses={201: UseUserItemSerializer(many=False)})
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        uid = self.request.resolver_match.kwargs['user_id']
        item = self.request.resolver_match.kwargs['item_id']
        action = request.data.get("action")
        if action != "ACTION_USE":
            return Response(status=404,
                            data={"message": "Такое действие невозможно осущесвтить"})
        stock = request.data.get("stock")
        message, response_status = inventory_change(uid, item, stock, action)
        return Response(status=response_status,
                        data=message)



