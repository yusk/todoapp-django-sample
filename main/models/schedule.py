from django.db import models
from django.core.exceptions import ValidationError
# from rest_framework.serializers import ValidationError


def validate_task(task):
    if Schedule.objects.filter(task=task).count() > 0:
        raise ValidationError("This task has already been registered.")


class Schedule(models.Model):
    task = models.ForeignKey("task",
                             on_delete=models.CASCADE,
                             validators=[validate_task])

    from_time = models.TimeField()
    to_time = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
