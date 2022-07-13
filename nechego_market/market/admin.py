from django.contrib import admin

# Register your models here.
from market.models import Item, Weapon

admin.site.register(Item)
admin.site.register(Weapon)