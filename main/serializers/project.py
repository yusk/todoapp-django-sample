from rest_framework import serializers

from main.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    task_ids = serializers.SerializerMethodField()
    done_task_ids = serializers.SerializerMethodField()
    not_done_task_ids = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'task_ids', 'done_task_ids', 'not_done_task_ids', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].read_only = True
        self.fields['description'].required = False

    def get_task_ids(self, obj):
        return [d.no for d in obj.tasks.all()]

    def get_done_task_ids(self, obj):
        return [d.no for d in obj.tasks.all().filter(done_at__isnull=False)]

    def get_not_done_task_ids(self, obj):
        return [d.no for d in obj.tasks.all().filter(done_at__isnull=True)]
