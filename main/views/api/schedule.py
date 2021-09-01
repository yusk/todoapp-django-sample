from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from main.models import Schedule
from main.serializers import ScheduleSerializer


class ScheduleFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(fields=(
        ('id', 'id'),
        ('from_time', 'from_time'),
        ('to_time', 'to_time'),
    ), )

    class Meta:
        model = Schedule
        fields = [
            "id",
            "from_time",
            "to_time",
        ]


class ScheduleViewSet(ModelViewSet):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.select_related("task")
    filter_class = ScheduleFilter
    ordering_fields = ('created_at', )
    ordering = ('created_at', )

    def get_serializer(self, *args, **kwargs):
        kwargs["user"] = self.request.user
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(task__user=self.request.user)
