from rest_framework import serializers

from main.models import Schedule, Task
from main.utils import with_method_class


class ScheduleSerializer(serializers.ModelSerializer):
    task_id = with_method_class(serializers.IntegerField)()

    class Meta:
        model = Schedule
        fields = ('id', 'task_id', 'from_time', 'to_time', )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields['id'].read_only = True

    def validate(self, data):
        task_id = data.pop("task_id")
        task = Task.objects.filter(no=task_id, user=self.user).first()
        if task is None:
            raise serializers.ValidationError({"task_id": "invalid task id"})
        data["task"] = task
        return data

    def get_task_id(self, obj):
        return obj.task.no
