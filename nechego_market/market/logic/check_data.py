from inventory.logic.remove_statuses import remove_expired_statuses
from market.logic.generate_item_list import generate_items_for_group, generate_items
from market.models import ItemInGroup, ChatGroup


class PrepareData(object):

    def get_queryset(self):
        generate_items()
        remove_expired_statuses()
        return super().get_queryset()


def create_group_or_filter(group_id: int) -> ItemInGroup:
    items = ItemInGroup.objects.filter(group__group_id=group_id)
    if not items:
        group = ChatGroup.objects.create(group_id=group_id)
        generate_items_for_group(group)
        items = ItemInGroup.objects.filter(group__group_id=group_id)
        return items
    return items
