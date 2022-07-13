from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=1024)  # имя товара

    # Указатели на минимальную и максимальную возможную цену
    min_price = models.IntegerField(blank=True, null=True)
    max_price = models.IntegerField(blank=True, null=True)
    # Сегодняшняя актуальная цена
    actual_price_today = models.IntegerField(blank=True, null=True)

    # Аналогично для кол-ва товара на сегодня
    min_stock = models.IntegerField(blank=True, null=True)
    max_stock = models.IntegerField(blank=True, null=True)
    actual_stock_today = models.IntegerField(blank=True, null=True)

    # Флаг, указывающий на тип предмета
    type_flag = models.CharField(max_length=512, blank=True, null=True)

    photo = models.ImageField()  # мб не надо?
    description = models.TextField()

    def __str__(self):
        return self.name


class Weapon(Item):
    damage = models.IntegerField()

    def __str__(self):
        return self.name
