from main.helpers.jwt import gen_jwt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema

from main.models import User
from main.serializers import UserSerializer, UserPasswordSerializer, TokenSerializer


class UserFilter(filters.FilterSet):
    name__gt = filters.CharFilter(field_name='name', lookup_expr='gt')
    name__lt = filters.CharFilter(field_name='name', lookup_expr='lt')

    order_by = filters.OrderingFilter(fields=(
        ('id', 'id'),
        ('name', 'name'),
    ), )

    class Meta:
        model = User
        fields = [
            "id",
            "name",
        ]


class UserView(GenericAPIView):
    serializer_class = UserSerializer

    @method_decorator(
        decorator=swagger_auto_schema(responses={200: UserSerializer}))
    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserPasswordView(GenericAPIView):
    serializer_class = UserPasswordSerializer

    @method_decorator(
        decorator=swagger_auto_schema(responses={200: TokenSerializer}))
    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user

        if not user.check_password(serializer.validated_data["password"]):
            return Response({"passowrd": "password not matched"})

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response({"token": gen_jwt(user)})


class UserViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_class = UserFilter
    ordering_fields = ('created_at', )
    ordering = ('created_at', )
