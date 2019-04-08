from django.db import models
from jsonfield import JSONField
from django.views.generic import TemplateView


class Bookmark(models.Model):
    title = models.CharField(max_length=100)
    thumbnail = models.CharField(max_length=100)
    content = models.TextField()
    url = models.CharField(max_length=100)
    tags = JSONField()

    def __str__(self):
        return self.title
