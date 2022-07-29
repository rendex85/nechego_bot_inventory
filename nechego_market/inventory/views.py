# Create your views here.
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response

from inventory.logic.remove_add_item import inventory_change
from inventory.models import UserItem, ConferenceUserStatus
from inventory.serializer import CreateUserItemSerializer, UseUserItemSerializer, UserItemSerializer, \
    ConferenceUserStatusSerializer
from market.logic.check_data import PrepareData
from market.serializer import ItemInfoSerializer


class InventoryList(PrepareData, generics.ListAPIView):
    """
    Список предметов в инвентаре пользователя
    """
    queryset = UserItem.objects.all()
    serializer_class = UserItemSerializer

    def get_queryset(self):
        items_group = UserItem.objects.filter(user__uid=self.request.resolver_match.kwargs['user_id'], stock__gt=0)
        super().get_queryset()
        return items_group

class StatusList(PrepareData, generics.ListAPIView):
    """
    Список предметов в инвентаре пользователя
    """
    queryset = ConferenceUserStatus.objects.all()
    serializer_class = ConferenceUserStatusSerializer

    def get_queryset(self):
        statuses = ConferenceUserStatus.objects.filter(user__uid=self.request.resolver_match.kwargs['user_id'])
        super().get_queryset()
        return statuses


class InventoryRetrieve(PrepareData, generics.RetrieveAPIView):
    """
    Конкретный предмет в инвентаре пользователя
    """
    queryset = UserItem.objects.all()
    serializer_class = ItemInfoSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        queryset = self.get_queryset()
        user = self.request.resolver_match.kwargs['user_id']
        item = self.request.resolver_match.kwargs['item_id']
        obj = get_object_or_404(queryset, user__id=user, item__id=item)
        return obj


class UseUserItem(PrepareData, generics.CreateAPIView):
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
                            data={"message": "Такое действие невозможно осуществить"})
        stock = request.data.get("stock") if request.data.get("stock") else 1

        message, response_status = inventory_change(uid, item, stock, action)
        return Response(status=response_status,
                        data=message)
