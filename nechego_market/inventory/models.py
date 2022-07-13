from django.db import models


# Create your models here.

class ConferenceUser(models.Model):
    uid = models.IntegerField(blank=True, null=True, unique=True)
    name = models.CharField(max_length=1024)

    def __str__(self):
        return str(self.uid)


class UserItem(models.Model):
    user = models.ForeignKey(ConferenceUser, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey("market.Item", on_delete=models.CASCADE)
    stock = models.IntegerField(blank=True, null=True, default=1)

