from django.db import models


# Create your models here.

class ConferenceUser(models.Model):
    uid = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class UserItem(models.Model):
    user = models.ForeignKey(ConferenceUser, on_delete=models.CASCADE)
    item = models.ForeignKey("market.Item", on_delete=models.CASCADE)
    used = models.BooleanField(default=False)

