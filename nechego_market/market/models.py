import datetime

from django.db import models


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class MarketUpdaterInfo(SingletonModel):
    last_updated = models.DateField(default=datetime.date(2019, 4, 13))
    nums_of_markets = models.IntegerField(blank=True, null=True)
    nums_of_users = models.IntegerField(blank=True, null=True)


class Item(models.Model):
    name = models.CharField(max_length=1024)  # имя товара

    # Указатели на минимальную и максимальную возможную цену
    min_price = models.IntegerField(blank=True, null=True)
    max_price = models.IntegerField(blank=True, null=True)
    # Сегодняшняя актуальная цена

    # Аналогично для кол-ва товара на сегодня
    min_stock = models.IntegerField(blank=True, null=True)
    max_stock = models.IntegerField(blank=True, null=True)

    # Флаг, указывающий на тип предмета
    type_flag = models.CharField(max_length=512, blank=True, null=True)

    smile = models.CharField(max_length=1024, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class ChatGroup(models.Model):
    group_id=models.IntegerField(blank=True, null=True)


class ItemInGroup(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    group = models.ForeignKey(ChatGroup, blank=True, null=True, on_delete=models.CASCADE)
    actual_price_today = models.IntegerField(blank=True, null=True)
    actual_stock_today = models.IntegerField(blank=True, null=True)


class Weapon(Item):
    damage = models.IntegerField()

    def __str__(self):
        return self.name
