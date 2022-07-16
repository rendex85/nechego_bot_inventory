from market.logic.generate_item_list import generate_items_for_group
from market.models import ItemInGroup, ChatGroup


def create_group_or_filter(group_id: int) -> ItemInGroup:
    items = ItemInGroup.objects.filter(group__group_id=group_id)
    if not items:
        group = ChatGroup.objects.create(group_id=group_id)
        generate_items_for_group(group)
    items = ItemInGroup.objects.filter(group__group_id=group_id)
    return items
