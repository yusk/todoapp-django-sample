from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from main.models import User
from main.serializers import TokenSerializer, UUIDSerializer
from main.helpers import gen_jwt


class AuthUUIDView(GenericAPIView):
    serializer_class = UUIDSerializer
    permission_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(device_uuid=serializer.data['uuid']).first()

        if user is None:
            message = {'detail': 'そのユーザーは存在しません'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        serializer = TokenSerializer(data={'token': gen_jwt(user)})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
