from django.contrib import admin

# Register your models here.
from inventory.models import ConferenceUser, UserItem

admin.site.register(ConferenceUser)
admin.site.register(UserItem)