from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from datetime import datetime

# Create your models here.
class Podcast(models.Model):
    title = models.CharField(max_length=256, unique=True)
    author = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    url = models.URLField()
    episodesSortOrder = models.IntegerField()
    language = models.CharField(max_length=64)
    categories = ArrayField(
        models.CharField(max_length=48, blank=True)
    )
    thumbnailurl = models.URLField(blank=True)
    thumbnailSmall = models.URLField(blank=True)
    mediatype = models.URLField(blank=True)

class Comment(models.Model):
    podcast = models.ForeignKey('podcasts.Podcast', related_name='comments', on_delete=models.DO_NOTHING)
    body = models.TextField(max_length=240)
    date = models.DateTimeField(default=datetime.now, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)