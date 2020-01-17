from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from datetime import datetime

# Create your models here.
class Podcast(models.Model):
    podcast_id = models.TextField(max_length=256, default="0", unique=True)


class Comment(models.Model):
    podcast = models.ForeignKey('podcasts.Podcast', related_name='comments', on_delete=models.DO_NOTHING, default="0")
    body = models.TextField(max_length=240)
    date = models.DateTimeField(default=datetime.now, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

class Like(models.Model):
    podcast = models.ForeignKey('podcasts.Podcast', related_name='likes', on_delete=models.DO_NOTHING, default=None, null=True)
    comment = models.ForeignKey('podcasts.Comment', related_name='likes', on_delete=models.DO_NOTHING, default=None, null=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)