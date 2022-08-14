from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.__class__.__name__ }({self.name})"
