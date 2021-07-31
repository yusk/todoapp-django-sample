from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from main.models import Tag
from main.serializers import NameSerializer


class TagViewSet(ListModelMixin, GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = NameSerializer

    def get_queryset(self):
        return super().get_queryset().filter(tasks__user=self.request.user)
