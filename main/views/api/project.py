from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from main.models import Project
from main.serializers import ProjectSerializer


class ProjectFilter(filters.FilterSet):
    name__gt = filters.CharFilter(field_name='name', lookup_expr='gt')
    name__lt = filters.CharFilter(field_name='name', lookup_expr='lt')

    order_by = filters.OrderingFilter(fields=(
        ('id', 'id'),
        ('title', 'name'),
    ), )

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
        ]


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.prefetch_related("tasks", "child_projects", "parent_projects")
    filter_class = ProjectFilter
    ordering_fields = ('created_at', )
    ordering = ('created_at', )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
