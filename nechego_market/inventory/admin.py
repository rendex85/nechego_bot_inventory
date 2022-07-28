from django.contrib import admin

# Register your models here.
from inventory.models import ConferenceUser, UserItem, ConferenceUserStatus

admin.site.register(ConferenceUser)
admin.site.register(UserItem)
admin.site.register(ConferenceUserStatus)
