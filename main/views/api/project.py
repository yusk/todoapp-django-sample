from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import Project
from main.serializers import ProjectSerializer, TaskSerializer


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
    queryset = Project.objects.prefetch_related("tasks", "child_projects",
                                                "parent_projects")
    filter_class = ProjectFilter
    ordering_fields = ('created_at', )
    ordering = ('created_at', )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    @action(detail=True, methods=['get'])
    def tasks(self, request, **kwargs):
        project = self.get_object()
        tasks = {}

        def get_task_data(task, visited: set):
            if task.id in tasks:
                return tasks[task.id]
            visited.add(task.id)
            task_data = TaskSerializer(task).data
            task_data["child_tasks"] = []
            for child_task in task.child_tasks.prefetch_related(
                    "projects", "child_tasks", "parent_tasks"):
                if child_task.id in visited:
                    continue
                task_data["child_tasks"].append(
                    get_task_data(child_task, visited))
            tasks[task.id] = task_data
            return task_data

        res = []
        for task in project.tasks.prefetch_related("projects", "child_tasks",
                                                   "parent_tasks"):
            if task.id not in tasks:
                tasks[id] = TaskSerializer(task).data
            visited = set()
            res.append(get_task_data(task, visited))
        return Response(res, status=200)
