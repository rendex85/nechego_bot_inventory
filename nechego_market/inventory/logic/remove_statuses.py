from datetime import datetime

from inventory.models import ConferenceUserStatus


def remove_expired_statuses():
    ConferenceUserStatus.objects.filter(time_limit__lt=datetime.now()).delete()