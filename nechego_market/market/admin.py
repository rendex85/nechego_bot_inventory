from django.contrib import admin

# Register your models here.
from market.models import Item, Weapon, MarketUpdaterInfo, ChatGroup, ItemInGroup, EffectItem, StatusItem

admin.site.register(Item)
admin.site.register(Weapon)
admin.site.register(MarketUpdaterInfo)
admin.site.register(ChatGroup)
admin.site.register(ItemInGroup)
admin.site.register(EffectItem)
admin.site.register(StatusItem)