import datetime
from typing import Tuple, Union

from django.db import transaction

from inventory.models import ConferenceUser, UserItem, ConferenceUserStatus
from market.models import Item, StatusItem, EffectItem
from market.serializer import ItemSmallSerializer, EffectSerializer


def remove_item(user: ConferenceUser, item_id: int, stock: int):
    try:
        invent_object = UserItem.objects.select_related("item").get(user=user, item_id=item_id)
        if invent_object.stock == 0:
            return {"message": "Такого предмета нет "}, 404
        elif invent_object.stock < stock:
            return {"message": "Такого предмета нет в таком количестве"}, 404
        else:
            invent_object.stock -= stock
            return {
                       "user_id": user.uid,
                       "item": ItemSmallSerializer(invent_object.item).data,
                       "stock": invent_object.stock}, 201
    except UserItem.DoesNotExist:
        return {"message": "Такого предмета нет"}, 404


def add_item(user: ConferenceUser, item_id: int, stock: int) -> Tuple[dict, int]:
    try:
        invent_object = UserItem.objects.select_related("item").get(user=user, item_id=item_id)
        invent_object.stock += stock

    except UserItem.DoesNotExist:
        invent_object = UserItem.objects.create(user=user, item_id=item_id, stock=stock)
    return {
               "user_id": user.uid,
               "item": ItemSmallSerializer(invent_object.item).data,
               "stock": invent_object.stock}, 201


def use_item(user: ConferenceUser, item_id: int) -> EffectItem:
    effect = EffectItem.objects.filter(item_on_effect__id=item_id)
    statuses = [e.status for e in effect if e.status]
    for status in statuses:
        ConferenceUserStatus.objects.create(user=user, status=status,
                                            time_limit=status.status_time + datetime.datetime.now())
    return effect


def inventory_change(uid: int, item_id: int, stock: int, flag: str) -> Tuple[dict, int]:
    try:
        user = ConferenceUser.objects.get(uid=uid)
    except ConferenceUser.DoesNotExist:
        user = ConferenceUser.objects.create(uid=uid)
    if flag == "ACTION_BUY":
        return add_item(user, item_id, stock)
    if flag == "ACTION_USE":
        message, status = remove_item(user, item_id, stock)
        if status == 201:
            effects = use_item(user, item_id)
            message["effects"] = EffectSerializer(effects, many=True).data
        return message, status
