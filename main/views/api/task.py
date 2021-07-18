from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404

from main.models import Task, Tag
from main.serializers import TaskSerializer, NameSerializer


class TaskFilter(filters.FilterSet):
    title__gt = filters.CharFilter(field_name='title', lookup_expr='gt')
    title__lt = filters.CharFilter(field_name='title', lookup_expr='lt')

    order_by = filters.OrderingFilter(fields=(
        ('id', 'id'),
        ('title', 'title'),
    ), )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
        ]


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.prefetch_related("projects", "child_tasks",
                                             "parent_tasks")
    filter_class = TaskFilter
    ordering_fields = ('created_at', )
    ordering = ('created_at', )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    @swagger_auto_schema(request_body=NameSerializer)
    @action(detail=True, methods=['post'], url_path="tag/add")
    def add_tag(self, request, pk=None):
        task = self.get_object()
        serializer = NameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag, _ = Tag.objects.get_or_create(name=serializer.data["name"])
        task.tags.add(tag)
        return Response(self.get_serializer(task).data)

    @swagger_auto_schema(request_body=NameSerializer)
    @action(detail=True, methods=['post'], url_path="tag/remove")
    def remove_tag(self, request, pk=None):
        task = self.get_object()
        serializer = NameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag, _ = Tag.objects.get_or_create(name=serializer.data["name"])
        task.tags.remove(tag)
        return Response(self.get_serializer(task).data)
