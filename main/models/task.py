from django.db import models


class Task(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField(default="")

    deadline = models.DateTimeField(null=True, db_index=True)
    done_at = models.DateTimeField(null=True, db_index=True)

    child_tasks = models.ManyToManyField("Task",
                                         through="TaskRelation",
                                         through_fields=("parent", "child"),
                                         related_name="parent_tasks",
                                         blank=True)
    projects = models.ManyToManyField("Project", related_name="tasks")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)


class TaskRelation(models.Model):
    parent = models.ForeignKey("Task",
                               related_name="parent",
                               on_delete=models.CASCADE)
    child = models.ForeignKey("Task",
                              related_name="child",
                              on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
