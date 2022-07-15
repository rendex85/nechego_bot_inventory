from rest_framework import serializers

from market.models import Item, Weapon


class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ["id", "damage"]


class ItemBaseSerializer(serializers.ModelSerializer):
    weapon = WeaponSerializer(many=False, required=False)

    class Meta:
        model = Item
        fields = "__all__"
