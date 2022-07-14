from rest_framework import serializers
from rest_framework.fields import IntegerField

from inventory.models import ConferenceUser, UserItem
from market.models import Item, Weapon


class ConferenceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConferenceUser
        fields = "__all__"


class CreateUserItemSerializer(serializers.Serializer):
    uid = IntegerField(write_only=True)
    item = IntegerField(write_only=True)
    stock = IntegerField(write_only=True)

    """def create(self, validated_data):
        print(validated_data)
        return UserItem.objects.create(**validated_data)

    class Meta:
        model = UserItem
        fields = ["uid", "item"]"""
