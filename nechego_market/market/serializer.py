from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField

from market.models import Item, Weapon, ItemInGroup


class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ["id", "damage"]


class ItemBaseSerializer(serializers.ModelSerializer):
    weapon = WeaponSerializer(many=False, required=False)

    class Meta:
        model = Item
        fields = "__all__"


class ItemSmallSerializer(serializers.ModelSerializer):
    # weapon = WeaponSerializer(many=False, required=False)

    class Meta:
        model = Item
        fields = ["id", "name", "smile"]


class ItemInGroupSerializer(serializers.ModelSerializer):
    item = ItemBaseSerializer(many=False, required=True)

    class Meta:
        model = ItemInGroup
        fields = "__all__"


class BuyItem(serializers.Serializer):
    action = CharField(write_only=True)
    user_id = IntegerField(write_only=True)
    stock = IntegerField(write_only=True, required=False)


class ResponseBuyItem(BuyItem):
    user_id = IntegerField()
    stock = IntegerField(required=False)
    item = ItemSmallSerializer(many=False)
