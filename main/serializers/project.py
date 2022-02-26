# from main.utils.djangoutils.serializer import with_method_class
from rest_framework import serializers

from main.models import Project
from main.utils import with_method_class


class ProjectSerializer(serializers.ModelSerializer):
    task_ids = serializers.SerializerMethodField()
    done_task_ids = serializers.SerializerMethodField()
    not_done_task_ids = serializers.SerializerMethodField()
    parent_project_ids = with_method_class(serializers.CharField)(required=False, help_text='e.g. "1,3"')
    child_project_ids = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'task_ids', 'done_task_ids', 'not_done_task_ids', 'parent_project_ids', 'child_project_ids', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].read_only = True
        self.fields['description'].required = False
        self.fields['parent_project_ids'].allow_blank = True

    def validate_parent_project_ids(self, value):
        if value == "":
            return []
        return [int(s.strip()) for s in value.split(",")]

    def create(self, validated_data):
        user = validated_data["user"]
        projects = None
        if 'parent_project_ids' in validated_data:
            parent_project_ids = validated_data.pop('parent_project_ids')
            projects = list(Project.objects.filter(id__in=parent_project_ids, user=user))
        instance = super().create(validated_data)
        if projects:
            instance.parent_projects.add(*projects)
        return instance

    def get_task_ids(self, obj):
        return [d.no for d in obj.tasks.all()]

    def get_done_task_ids(self, obj):
        return [d.no for d in obj.tasks.all().filter(done_at__isnull=False)]

    def get_not_done_task_ids(self, obj):
        return [d.no for d in obj.tasks.all().filter(done_at__isnull=True)]

    def get_parent_project_ids(self, obj):
        return [d.id for d in obj.parent_projects.all()]

    def get_child_project_ids(self, obj):
        return [d.id for d in obj.child_projects.all()]
