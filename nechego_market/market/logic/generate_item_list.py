import datetime
import random

from market.models import MarketUpdaterInfo, ItemInGroup, ChatGroup, Item


def generate_items_for_group(group):
    items_number = random.randint(3, 5)
    today_items = Item.objects.all().order_by('?')[:items_number]
    for item in today_items:
        today_stock = random.randint(item.min_stock, item.max_stock)
        today_price = random.randint(item.min_price, item.max_price)
        ItemInGroup.objects.create(group=group, item=item, actual_price_today=today_price,
                                   actual_stock_today=today_stock)


def generate_items():
    update_object = MarketUpdaterInfo.load()
    today_day = datetime.datetime.today()
    if today_day.day != update_object.last_updated.day:
        update_object.last_updated = today_day
        update_object.save()
        ItemInGroup.objects.all().delete()
        for group in ChatGroup.objects.all():
            generate_items_for_group(group)
