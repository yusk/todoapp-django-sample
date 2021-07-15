from rest_framework import serializers

from main.models import Task
from main.utils import with_method_class


class TaskSerializer(serializers.ModelSerializer):
    parent_task_ids = with_method_class(serializers.CharField)(required=False, help_text='e.g. "1,3"')
    child_task_ids = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'parent_task_ids', 'child_task_ids', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].read_only = True
        self.fields['description'].required = False

    def create(self, validated_data):
        tasks = None
        if 'parent_task_ids' in validated_data:
            parent_task_ids = validated_data.pop('parent_task_ids')
            parent_task_ids = [int(task_id.strip()) for task_id in parent_task_ids.split(",")]
            tasks = list(Task.objects.filter(id__in=parent_task_ids))
        instance = super().create(validated_data)
        if tasks:
            instance.parent_tasks.add(*tasks)
        return instance

    def update(self, instance, validated_data):
        if 'parent_task_ids' in validated_data:
            parent_task_ids = validated_data.pop('parent_task_ids')
            parent_task_ids = [int(task_id.strip()) for task_id in parent_task_ids.split(",")]
            tasks = list(Task.objects.filter(id__in=parent_task_ids))
            instance.parent_tasks.add(*tasks)
        return super().update(instance, validated_data)

    def get_parent_task_ids(self, obj):
        return [d["id"] for d in obj.parent_tasks.all().values("id")]

    def get_child_task_ids(self, obj):
        return [d["id"] for d in obj.child_tasks.all().values("id")]
