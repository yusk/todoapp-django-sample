from django.db import models


class Project(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField(default="")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
