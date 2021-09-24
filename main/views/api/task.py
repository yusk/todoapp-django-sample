from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema

from main.models import Task, Tag
from main.serializers import TaskSerializer, NoneSerializer, NameSerializer
from main.utils import get_by_manytomany


class TaskFilter(filters.FilterSet):
    def is_empty(self, queryset, name, value):
        assert name[-8:] == "_isempty"
        params = {name[:-8]: ""}
        if value:
            return queryset.filter(**params)
        else:
            return queryset.exclude(**params)

    def get_by_manytomany0(self, queryset, name, value):
        return get_by_manytomany(queryset, name, value, 0)

    def get_by_manytomany1_no(self, queryset, name, value):
        name = name.replace("_id", "_no")
        return get_by_manytomany(queryset, name, value, 1)

    title_icontains = filters.CharFilter(field_name='title',
                                         lookup_expr='icontains')
    description_icontains = filters.CharFilter(field_name='description',
                                               lookup_expr='icontains')
    description_isempty = filters.BooleanFilter(method='is_empty')

    deadline_year = filters.NumberFilter(field_name='deadline',
                                         lookup_expr='year')
    deadline_month = filters.NumberFilter(field_name='deadline',
                                          lookup_expr='month')
    deadline_day = filters.NumberFilter(field_name='deadline',
                                        lookup_expr='day')
    deadline_date = filters.DateFilter(field_name='deadline',
                                       lookup_expr='date')
    deadline_gt = filters.DateTimeFilter(field_name='deadline',
                                         lookup_expr='gt')
    deadline_lt = filters.DateTimeFilter(field_name='deadline',
                                         lookup_expr='lt')
    deadline_isnull = filters.BooleanFilter(field_name='deadline',
                                            lookup_expr='isnull')

    done_at_year = filters.NumberFilter(field_name='done_at',
                                        lookup_expr='year')
    done_at_month = filters.NumberFilter(field_name='done_at',
                                         lookup_expr='month')
    done_at_day = filters.NumberFilter(field_name='done_at', lookup_expr='day')
    done_at_date = filters.DateFilter(field_name='done_at', lookup_expr='date')
    done_at_gt = filters.DateTimeFilter(field_name='done_at', lookup_expr='gt')
    done_at_lt = filters.DateTimeFilter(field_name='done_at', lookup_expr='lt')
    done_at_isnull = filters.BooleanFilter(field_name='done_at',
                                           lookup_expr='isnull')

    child_task_id = filters.NumberFilter(method='get_by_manytomany1_no')
    child_task_id_isnull = filters.BooleanFilter(field_name='child_tasks',
                                                 lookup_expr='isnull')
    parent_task_id = filters.NumberFilter(method='get_by_manytomany1_no')
    parent_task_id_isnull = filters.BooleanFilter(field_name='parent_tasks',
                                                  lookup_expr='isnull')
    project_id = filters.NumberFilter(method='get_by_manytomany0')
    project_id_isnull = filters.BooleanFilter(field_name='projects',
                                              lookup_expr='isnull')
    tag_name = filters.CharFilter(method='get_by_manytomany0')
    tag_isnull = filters.BooleanFilter(field_name='tags', lookup_expr='isnull')

    order_by = filters.OrderingFilter(fields=(
        ('id', 'id'),
        ('no', 'no'),
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

    lookup_field = 'no'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).distinct()

    @swagger_auto_schema(request_body=NoneSerializer)
    @action(detail=True, methods=['post'])
    def done(self, request, **kwargs):
        task = self.get_object()
        task.done_at = timezone.now()
        task.save()
        return Response(self.get_serializer(task).data)

    @swagger_auto_schema(request_body=NoneSerializer)
    @action(detail=True, methods=['post'])
    def undone(self, request, **kwargs):
        task = self.get_object()
        task.done_at = None
        task.save()
        return Response(self.get_serializer(task).data)

    @swagger_auto_schema(request_body=NameSerializer)
    @action(detail=True, methods=['post'], url_path="tag/add")
    def add_tag(self, request, **kwargs):
        task = self.get_object()
        serializer = NameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag, _ = Tag.objects.get_or_create(name=serializer.data["name"])
        task.tags.add(tag)
        return Response(self.get_serializer(task).data)

    @swagger_auto_schema(request_body=NameSerializer)
    @action(detail=True, methods=['post'], url_path="tag/remove")
    def remove_tag(self, request, **kwargs):
        task = self.get_object()
        serializer = NameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag, _ = Tag.objects.get_or_create(name=serializer.data["name"])
        task.tags.remove(tag)
        return Response(self.get_serializer(task).data)
