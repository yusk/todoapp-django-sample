from django.utils import timezone
from django_filters.fields import Lookup
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema

from main.models import Task, Tag
from main.serializers import TaskSerializer, NoneSerializer, NameSerializer


class TaskFilter(filters.FilterSet):
    def get_by_manytomany(self, queryset, name, value):
        v = name.split("_")
        model_name = f"{v[0]}s"
        key = v[1]
        kwargs = {f"{model_name}__{key}": value}
        return queryset.filter(**kwargs).distinct()

    deadline_gt = filters.DateTimeFilter(field_name='deadline',
                                         lookup_expr='gt')
    deadline_lt = filters.DateTimeFilter(field_name='deadline',
                                         lookup_expr='lt')
    deadline_isnull = filters.BooleanFilter(field_name='deadline',
                                            lookup_expr='isnull')

    done_at_gt = filters.DateTimeFilter(field_name='done_at', lookup_expr='gt')
    done_at_lt = filters.DateTimeFilter(field_name='done_at', lookup_expr='lt')
    done_at_isnull = filters.BooleanFilter(field_name='done_at',
                                           lookup_expr='isnull')

    tag_name = filters.CharFilter(method='get_by_manytomany')
    project_id = filters.NumberFilter(method='get_by_manytomany')
    project_id_isnull = filters.BooleanFilter(field_name='projects',
                                              lookup_expr='isnull')

    order_by = filters.OrderingFilter(fields=(
        ('id', 'id'),
        ('title', 'title'),
        ('deadline', 'deadline'),
        ('done_at', 'done_at'),
        ('created_at', 'created_at'),
    ), )

    class Meta:
        model = Task
        fields = [
            "id",
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

    @swagger_auto_schema(request_body=NoneSerializer)
    @action(detail=True, methods=['post'])
    def done(self, request, pk=None):
        task = self.get_object()
        task.done_at = timezone.now()
        task.save()
        return Response(self.get_serializer(task).data)

    @swagger_auto_schema(request_body=NoneSerializer)
    @action(detail=True, methods=['post'])
    def undone(self, request, pk=None):
        task = self.get_object()
        task.done_at = None
        task.save()
        return Response(self.get_serializer(task).data)

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
