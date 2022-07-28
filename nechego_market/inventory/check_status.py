from datetime import datetime

from inventory.models import ConferenceUserStatus


def status_end():
    statuses = ConferenceUserStatus.objects.all()
    for status in statuses:
        if datetime.now() > status.time_limit:
            status.delete()
