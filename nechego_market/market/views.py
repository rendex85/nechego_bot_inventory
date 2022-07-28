# Create your views here.
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response

from inventory.models import UserItem
from market.logic.buy_sell_items import buy_item
from market.logic.create_data import create_group_or_filter
from market.logic.generate_item_list import generate_items
from market.models import ItemInGroup
from market.serializer import ItemInGroupSerializer, BuyItem, ResponseBuyItem


class ItemInGroupListView(generics.ListAPIView):
    """Возвращает список предметов, доступных для покупки в конференции на сегодня"""
    queryset = ItemInGroup.objects.all()
    serializer_class = ItemInGroupSerializer

    def get_queryset(self):
        generate_items()
        items_group = create_group_or_filter(self.request.resolver_match.kwargs['group_id'])
        return items_group.order_by("id")


class CreateUserItem(generics.CreateAPIView):
    """
    Покупка предмета.

    action - возможное действие с предметом
    user_id - id пользователя внутри сервисов
    stock - количество предметов которые надо купить. 1 по умолчанию
    stock_in_inventory - сколько предметов находится у пользователя

    """
    queryset = UserItem.objects.all()
    serializer_class = BuyItem

    @swagger_auto_schema(responses={201: ResponseBuyItem(many=False)})
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        generate_items()
        uid = request.data.get("user_id")
        # TODO: сделать что-то с акшном
        action = request.data.get("action")
        stock = request.data.get("stock")
        item_id = request.resolver_match.kwargs["item_id"]
        group_id = request.resolver_match.kwargs["group_id"]

        message, response_status = buy_item(uid=uid, group_id=group_id, item_id=item_id, stock=stock, flag=action)

        return Response(status=response_status,
                        data=message)
