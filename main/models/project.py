from django.db import models


class Project(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    child_projects = models.ManyToManyField("Project",
                                            through="ProjectRelation",
                                            through_fields=("parent", "child"),
                                            related_name="parent_projects",
                                            blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)


class ProjectRelation(models.Model):
    parent = models.ForeignKey("Project",
                               related_name="parent",
                               on_delete=models.CASCADE)
    child = models.ForeignKey("Project",
                              related_name="child",
                              on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["parent", "child"],
                                    name="uq_project_parent_child"),
        ]
