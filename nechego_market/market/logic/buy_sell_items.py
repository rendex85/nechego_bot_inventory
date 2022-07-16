from typing import Tuple, Union

from inventory.remove_add_item import inventory_change
from market.logic.create_data import create_group_or_filter


def buy_item(uid: int, group_id: int, item_id: int, stock: Union[int, None]) -> Tuple[dict, int]:
    item_group_object = create_group_or_filter(group_id=group_id).filter(item_id=item_id)

    if not stock:
        stock = 1
    if not item_group_object:
        return {"message": "Данного предмета сейчас нет в продаже"}, 404
    else:
        item_group = item_group_object[0]

    if item_group.actual_stock_today < stock:
        return {"message": "Данного предмета нет в таком количестве."}, 404
    else:
        item_group.actual_stock_today -= stock
        item_group.save()
        return inventory_change(uid, item_id, stock, "add")
