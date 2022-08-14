from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

import calendar
from copy import deepcopy
from datetime import timedelta, date


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return d + timedelta(days=days_ahead)


class Repeat(models.Model):
    WEEKS = list(calendar.day_name)

    class Type(models.TextChoices):
        DAY = 'DAY', 'DAY'
        WEEK = 'WEEK', 'WEEK'
        MONTH = 'MONTH', 'MONTH'
        YEAR = 'YEAR', 'YEAR'

    type = models.CharField(max_length=15, choices=Type.choices)
    n = models.IntegerField()  # n 日ごと, 毎月 n 週目, 毎月 n 日, 毎年 n 月
    m = models.IntegerField(null=True, blank=True)  # 毎月第 n m 曜日, 毎年 n 月 m 日

    end_date = models.DateField(null=True, blank=True)
    repeat_num = models.IntegerField(null=True, blank=True)

    def __str__(self):
        s = self.__class__.__name__ + "({})"
        if self.type == Repeat.Type.DAY:
            return s.format(f"{self.n}日ごと")
        elif self.type == Repeat.Type.WEEK:
            return s.format(f"毎週 {self.WEEKS[self.n]}")
        elif self.type == Repeat.Type.MONTH:
            if self.m is None:
                return s.format(f"毎月{self.n}日")
            else:
                return s.format(f"毎月第{self.n} {self.WEEKS[self.m]}")
        elif self.type == Repeat.Type.YEAR:
            return s.format(f"毎年{self.n}月{self.m}日")
        raise AssertionError("invalid type")

    def clean(self):
        if self.type == self.Type.WEEK:
            if self.n < 0 or 6 < self.n:
                raise ValidationError({'n': "n need to be between 0 to 6"})
        elif self.type == self.Type.MONTH:
            if self.m is None:
                if self.n < 1 or 31 < self.n:
                    raise ValidationError(
                        {'n': "n need to be between 1 to 31"})
            else:
                raise ValidationError({'m': "m need to be between 0 to 6"})
        elif self.type == 'YEAR':
            if self.m is None:
                raise ValidationError({'m': "m required"})
            elif self.n < 1 or 12 < self.n:
                raise ValidationError({'n': "n need to be between 1 to 12"})
            elif self.m < 1 or 31 < self.m:  # todo: impl day of month validation
                raise ValidationError({'m': "m need to be between 1 to 31"})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Task(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    no = models.IntegerField()

    title = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)

    deadline_date = models.DateField(null=True, blank=True, db_index=True)
    deadline_time = models.TimeField(null=True, blank=True, db_index=True)
    done_at = models.DateTimeField(null=True, blank=True, db_index=True)

    repeat = models.ForeignKey("Repeat",
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)

    child_tasks = models.ManyToManyField("Task",
                                         through="TaskRelation",
                                         through_fields=("parent", "child"),
                                         related_name="parent_tasks",
                                         blank=True)
    projects = models.ManyToManyField("Project",
                                      related_name="tasks",
                                      blank=True)
    tags = models.ManyToManyField("Tag", related_name="tasks", blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def gen_repeat_task(self):
        if self.repeat is None:
            return False
        if self.repeat.repeat_num and self.repeat.repeat_num < 0:
            return False

        task = deepcopy(self)
        today = timezone.localdate()
        if self.repeat.type == Repeat.Type.DAY:
            task.deadline_date = today + timedelta(days=self.repeat.n)
        elif self.repeat.type == Repeat.Type.WEEK:
            task.deadline_date = next_weekday(today, self.repeat.n)
        elif self.repeat.type == Repeat.Type.MONTH:
            if self.repeat.m is None:
                if today.month == 12:
                    task.deadline_date = date(today.year + 1, 1, self.repeat.n)
                else:
                    task.deadline_date = date(today.year, today.month + 1,
                                              self.repeat.n)
            else:
                if today.month == 12:
                    next_month = date(today.year + 1, 1, 1)
                else:
                    next_month = date(today.year, today.month, 1)
                d = next_weekday(next_month, self.repeat.m)
                task.deadline_date = d + timedelta(days=(self.repeat.n - 1) *
                                                   7)
        elif self.repeat.type == Repeat.Type.YEAR:
            task.deadline_date = date(today.year + 1, self.repeat.n,
                                      self.repeat.m)
        else:
            return False

        if task.repeat.end_date and task.repeat.end_date > task.repeat.end_date:
            return False
        if task.repeat.repeat_num:
            repeat_num = task.repeat.repeat_num - 1
            if repeat_num <= 0:
                task.repeat = None
            else:
                repeat = deepcopy(task.repeat)
                repeat.id = None
                repeat.repeat_num = repeat_num
                repeat.save()
                task.repeat = repeat

        task.id = None
        task.no = self.next_no(task.user)
        task.save()
        return True

    def done(self):
        if self.done_at is None:
            self.done_at = timezone.now()
            self.save()
            self.gen_repeat_task()

    def undone(self):
        if self.done_at:
            self.done_at = None
            self.save()

    @classmethod
    def next_no(cls, user):
        data = cls.objects.filter(
            user=user).order_by("-no").values("no").first()
        print(data)
        if data is None:
            return 1
        return data["no"] + 1

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "no"],
                                    name="task_user_no_unique"),
        ]
        indexes = [models.Index(fields=['user', 'no'])]


class TaskRelation(models.Model):
    parent = models.ForeignKey("Task",
                               related_name="parent",
                               on_delete=models.CASCADE)
    child = models.ForeignKey("Task",
                              related_name="child",
                              on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["parent", "child"],
                                    name="uq_task_parent_child"),
        ]
