from rest_framework import serializers
from rest_framework.fields import IntegerField, CharField

from inventory.models import ConferenceUser, UserItem, ConferenceUserStatus
from market.serializer import ItemSmallSerializer, ItemInfoSerializer, EffectSerializer, StatusSerializer


class ConferenceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConferenceUser
        fields = "__all__"


class ConferenceUserStatusSerializer(serializers.ModelSerializer):
    status = StatusSerializer(many=False)

    class Meta:
        model = ConferenceUserStatus
        fields = "__all__"


class CreateUserItemSerializer(serializers.Serializer):
    action = CharField(write_only=True)


class UseUserItemSerializer(serializers.Serializer):
    user_id = IntegerField()
    stock_in_inventory = IntegerField(required=False)
    effect = EffectSerializer(many=True)


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
