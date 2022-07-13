# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from inventory.models import UserItem, ConferenceUser
from inventory.serializer import CreateUserItemSerializer


class CreateUserItem(generics.CreateAPIView):
    """
    View для получения и отправки комментариев
    Комментарии можно получить или отправить, указав в адресе id экспертизы,
    При желании можно в параметрах указать блок комментариев для GET-запроса
    """
    queryset = UserItem.objects.all()
    serializer_class = CreateUserItemSerializer

    def create(self, request, *args, **kwargs):
        uid = request.data["uid"]
        item = request.data["item"]
        try:
            user = ConferenceUser.objects.get(uid=uid)
        except ConferenceUser.DoesNotExist:
            user = ConferenceUser.objects.create(uid=uid)
        #TODO: здесь должена быть проверка, есть ли переданный айтем в стоке или нет
        try:
            invent_object = UserItem.objects.get(user=user, item_id=item)
            invent_object.stock += 1
            invent_object.save()
        except UserItem.DoesNotExist:
            invent_object = UserItem.objects.create(user=user, item_id=item)

        return Response(status=status.HTTP_200_OK, data={"message": f"Предмет {item} успешно добавлен в инвентарь {uid}"})
