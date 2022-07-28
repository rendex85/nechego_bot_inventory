from rest_framework import serializers
from rest_framework.fields import IntegerField

from inventory.models import ConferenceUser, UserItem
from market.serializer import ItemBaseSerializer, ItemSmallSerializer, ItemInfoSerializer


class ConferenceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConferenceUser
        fields = "__all__"


class CreateUserItemSerializer(serializers.Serializer):
    uid = IntegerField(write_only=True)
    item = IntegerField(write_only=True)
    stock = IntegerField(write_only=True)


class UseUserItemSerializer(serializers.Serializer):
    uid = IntegerField(write_only=True)
    item = IntegerField(write_only=True)
    stock = IntegerField(write_only=True)
    item_object = ItemBaseSerializer(many=False)


class UserItemSerializer(serializers.ModelSerializer):
    item = ItemSmallSerializer(many=False)

    class Meta:
        model = UserItem
        fields = "__all__"


class UserRetrieveSerializer(serializers.ModelSerializer):
    item = ItemInfoSerializer(many=False)

    class Meta:
        model = UserItem
        fields = "__all__"
