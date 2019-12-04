from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Podcast(models.Model):
    title = models.CharField(max_length=256)
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