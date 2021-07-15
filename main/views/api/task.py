from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from main.models import Task
from main.serializers import TaskSerializer


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
    queryset = Task.objects.all()
    filter_class = TaskFilter
    ordering_fields = ('created_at', )
    ordering = ('created_at', )

    def perform_create(self, serializer):
        print("perform_create")
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
