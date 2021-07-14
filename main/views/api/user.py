from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import schema
from rest_framework.schemas import ManualSchema
from django_filters import rest_framework as filters

from main.models import User
from main.serializers import UserSerializer


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

    @schema(ManualSchema(fields=[]))
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_class = UserFilter
    ordering_fields = ('created_at', )
    ordering = ('created_at', )
