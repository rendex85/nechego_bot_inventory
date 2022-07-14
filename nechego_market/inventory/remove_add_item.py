from typing import Tuple

from inventory.models import ConferenceUser, UserItem


def inventory_change(uid: int, item_id: int, stock: int, add_remove_flag: str) -> Tuple[dict, int]:
    try:
        user = ConferenceUser.objects.get(uid=uid)
    except ConferenceUser.DoesNotExist:
        user = ConferenceUser.objects.create(uid=uid)

    try:
        invent_object = UserItem.objects.get(user=user, item_id=item_id)
        if add_remove_flag == "add":
            invent_object.stock += stock
        elif add_remove_flag == "remove":
            if invent_object.stock == 0 or invent_object.stock < stock:
                return {"message": "Такого предмета нет в таком количестве"}, 404
            else:
                invent_object.stock -= stock
        else:
            return {"message": "Такого флага нет"}, 404

        invent_object.save()
    except UserItem.DoesNotExist:
        if add_remove_flag == "remove":
            return {"message": "Такого предмета нет"}, 404
        invent_object = UserItem.objects.create(user=user, item_id=item_id, stock=stock)

    return {
               "uid": uid,
               "item": item_id,
               "stock": invent_object.stock}, 201
