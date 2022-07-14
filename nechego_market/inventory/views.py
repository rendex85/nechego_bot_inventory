# Create your views here.
from rest_framework import generics
from rest_framework.response import Response

from inventory.models import UserItem
from inventory.remove_add_item import inventory_change
from inventory.serializer import CreateUserItemSerializer
from market.models import Item


class CreateUserItem(generics.CreateAPIView):
    """
    Добавление/покупка айтема
    поле stock в возвращаемых параметрах показывает актуальное количество предметов у пользователя
    """
    queryset = UserItem.objects.all()
    serializer_class = CreateUserItemSerializer

    def create(self, request, *args, **kwargs):
        uid = request.data["uid"]
        item = request.data["item"]
        stock = request.data["stock"]
        item_object = Item.objects.get(id=item)
        if item_object.actual_stock_today < stock:
            return Response(status=404,
                            data={"message": "Данного предмета нет в таком количестве."})
        else:
            item_object.actual_stock_today -= stock
            item_object.save()
        message, response_status = inventory_change(uid, item, stock, "add")

        return Response(status=response_status,
                        data=message)


class UseUserItem(generics.CreateAPIView):
    """
    Использование айтема
    поле stock в возвращаемых параметрах показывает актуальное количество предметов у пользователя
    """
    queryset = UserItem.objects.all()
    serializer_class = CreateUserItemSerializer

    def create(self, request, *args, **kwargs):
        uid = request.data["uid"]
        item = request.data["item"]
        stock = request.data["stock"]
        message, response_status = inventory_change(uid, item, stock, "remove")

        return Response(status=response_status,
                        data=message)
