# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response

from inventory.models import UserItem
from inventory.remove_add_item import inventory_change
from inventory.serializer import CreateUserItemSerializer, UseUserItemSerializer
from market.models import Item
from market.serializer import ItemBaseSerializer


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
        try:
            item_object = Item.objects.get(id=item)
        except Item.DoesNotExist:
            return Response(status=404,
                            data={"message": "Данного предмета не существует."})
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

    @swagger_auto_schema(responses={201: UseUserItemSerializer(many=False)})
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        uid = request.data["uid"]
        item = request.data["item"]
        stock = request.data["stock"]
        try:
            item_object = Item.objects.get(id=item)
        except Item.DoesNotExist:
            return Response(status=404,
                            data={"message": "Данного предмета не существует."})
        message, response_status = inventory_change(uid, item, stock, "remove")

        message["item_object"] = ItemBaseSerializer(item_object).data

        return Response(status=response_status,
                        data=message)
