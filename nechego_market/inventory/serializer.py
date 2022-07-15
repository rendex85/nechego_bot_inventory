from rest_framework import serializers
from rest_framework.fields import IntegerField

from inventory.models import ConferenceUser
from market.serializer import ItemBaseSerializer


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

