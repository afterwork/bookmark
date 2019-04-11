from django.db import models
from jsonfield import JSONField
from django.conf import settings


class Bookmark(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to="pictures/")
    content = models.TextField()
    url = models.URLField()
    pub_date = models.DateTimeField(auto_now=True)
    tags = JSONField()

    def __str__(self):
        return self.title
