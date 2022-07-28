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


class StatusItem(models.Model):
    STATUS_CHOICES = ((1, "Вас не может атаковать пользователь X."),
                      (2, "Вас не могут атаковать бедные пользователи."),
                      (3, "Вас не может атаковать магнат."),
                      (4, "Вас не может атаковать админ."),
                      (5, "Вас нельзя атаковать, если у вас нет энергии."),
                      (6, "Вас нельзя атаковать, если у вас полная энергия."),
                      (7, "Вас нельзя атаковать, если вы магнат."),
                      (8, "Вас нельзя атаковать, если вы не играли сегодня в казино."),
                      (9, "Вы сильнее на X."),
                      (10, "Вы слабее на X."),
                      (11, "Вы получаете на X монет больше при победе в кости."),
                      (12, "С вероятностью X%, вы не потратите энергии при атаке."),
                      (13, "с вероятностью X%, вы не потратите энергии при рыбалке."),
                      (14, "Вы не можете рыбачить."),
                      (15, "Вы не можете атаковать других."),
                      (16, "Вы не можете играть в казино."),
                      (17, "Вы не можете брать кредит."))
    status = models.IntegerField(max_length=1024, choices=STATUS_CHOICES, blank=True, null=True)
    status_value = models.IntegerField(blank=True, null=True)
    status_time = models.DurationField(blank=True, null=True)

    def __str__(self):
        return self.get_status_display() if not self.status_value else self.get_status_display().replace(
            "X", str(self.status_value))


class EffectItem(models.Model):
    EFFECT_CHOICES = ((1, "Восстановление энергии."),
                      (2, "Понижение энергии."),
                      (3, "Пополнение количества еды."),
                      (4, "Понижение количества еда."),
                      (5, "Наложение статуса (баффа или дебаффа)."),
                      (6, "Пополнение баланса."),
                      (7, "Списание с баланса."),
                      (8, "Пополнение банковского счета."),
                      (9, "Списание с банковского счета."),
                      (10, "Повышение кредита."),
                      (11, "Погашение кредита."))

    effect = models.IntegerField(max_length=1024, choices=EFFECT_CHOICES, blank=True, null=True)
    effect_value = models.IntegerField(blank=True, null=True)
    status = models.ForeignKey(StatusItem, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        effect = self.get_effect_display()
        if self.status:
            return effect + str(self.status)
        else:
            return effect + str(self.effect_value)


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

    effect = models.ManyToManyField(EffectItem, related_name="item_on_effect")

    def __str__(self):
        return self.name


class ChatGroup(models.Model):
    group_id = models.IntegerField(blank=True, null=True)


class ItemInGroup(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    group = models.ForeignKey(ChatGroup, blank=True, null=True, on_delete=models.CASCADE)
    actual_price_today = models.IntegerField(blank=True, null=True)
    actual_stock_today = models.IntegerField(blank=True, null=True)


class Weapon(Item):
    damage = models.IntegerField()

    def __str__(self):
        return self.name
