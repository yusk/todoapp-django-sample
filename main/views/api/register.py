from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_jwt.settings import api_settings
from drf_yasg.utils import swagger_auto_schema

from main.models import User
from main.serializers import NoneSerializer, TokenSerializer, UUIDSerializer, UserSignUpSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class RegisterDummyUserView(GenericAPIView):
    serializer_class = NoneSerializer
    permission_classes = ()

    @method_decorator(
        decorator=swagger_auto_schema(responses={200: TokenSerializer}))
    def post(self, request):
        user = User.objects.create_guest_user()
        user.name = 'dummy user'
        user.save()

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        serializer = TokenSerializer(data={'token': token})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class RegisterUUIDView(GenericAPIView):
    serializer_class = UUIDSerializer
    permission_classes = ()

    @method_decorator(
        decorator=swagger_auto_schema(responses={200: TokenSerializer}))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if User.objects.filter(device_uuid=serializer.data['uuid']):
            message = {'detail': 'すでにそのユーザーは登録済みです。'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_guest_user(
            device_uuid=serializer.data['uuid'])
        user.save()

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        serializer = TokenSerializer(data={'token': token})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class RegisterUserView(GenericAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = ()

    @method_decorator(
        decorator=swagger_auto_schema(responses={200: TokenSerializer}))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"])
        user.save()

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        serializer = TokenSerializer(data={'token': token})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
