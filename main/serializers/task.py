from rest_framework import serializers

from main.models import Task, Project, Tag
from main.utils import with_method_class


class TaskSerializer(serializers.ModelSerializer):
    parent_task_ids = with_method_class(serializers.CharField)(required=False, help_text='e.g. "1,3"')
    child_task_ids = serializers.SerializerMethodField(read_only=True)
    project_ids = with_method_class(serializers.CharField)(required=False, help_text='e.g. "1,3"')
    tags = with_method_class(serializers.CharField)(required=False, help_text='e.g. "tag1,tag2"')

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'deadline', 'done_at', 'parent_task_ids', 'child_task_ids', 'project_ids', 'tags', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].read_only = True
        self.fields['description'].required = False
        self.fields['done_at'].required = False
        self.fields['done_at'].read_only = False
        self.fields['deadline'].read_only = True

    def create(self, validated_data):
        tasks = None
        if 'parent_task_ids' in validated_data:
            parent_task_ids = validated_data.pop('parent_task_ids')
            parent_task_ids = [int(task_id.strip()) for task_id in parent_task_ids.split(",")]
            tasks = list(Task.objects.filter(id__in=parent_task_ids))
        projects = None
        if 'project_ids' in validated_data:
            project_ids = validated_data.pop('project_ids')
            project_ids = [int(project_id.strip()) for project_id in project_ids.split(",")]
            projects = list(Project.objects.filter(id__in=project_ids))
        tags = None
        if 'tags' in validated_data:
            tag_names = validated_data.pop('tags')
            tag_names = [tag_name.strip() for tag_name in tag_names.split(",")]
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag)
        instance = super().create(validated_data)
        if tasks:
            instance.parent_tasks.add(*tasks)
        if projects:
            instance.projects.add(*projects)
        if tags:
            instance.tags.add(*tags)
        return instance

    def update(self, instance, validated_data):
        if 'parent_task_ids' in validated_data:
            parent_task_ids = validated_data.pop('parent_task_ids')
            parent_task_ids = [int(task_id.strip()) for task_id in parent_task_ids.split(",")]
            tasks = list(Task.objects.filter(id__in=parent_task_ids))
            instance.parent_tasks.add(*tasks)
            tasks = instance.parent_tasks.exclude(id__in=parent_task_ids)
            instance.parent_tasks.remove(*tasks)
        if 'project_ids' in validated_data:
            project_ids = validated_data.pop('project_ids')
            project_ids = [int(project_id.strip()) for project_id in project_ids.split(",")]
            projects = list(Project.objects.filter(id__in=project_ids))
            instance.projects.add(*projects)
            projects = instance.projects.exclude(id__in=project_ids)
            instance.projects.remove(*projects)
        if 'tags' in validated_data:
            tag_names = validated_data.pop('tags')
            tag_names = [tag_name.strip() for tag_name in tag_names.split(",")]
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag)
            instance.tags.add(*tags)
            tags = instance.tags.exclude(name__in=tag_names)
            instance.tags.remove(*tags)
        return super().update(instance, validated_data)

    def get_parent_task_ids(self, obj):
        return [d.id for d in obj.parent_tasks.all()]

    def get_child_task_ids(self, obj):
        return [d.id for d in obj.child_tasks.all()]

    def get_project_ids(self, obj):
        return [d.id for d in obj.projects.all()]

    def get_tags(self, obj):
        return [d.name for d in obj.tags.all()]
