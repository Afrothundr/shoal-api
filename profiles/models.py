from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=256, blank=True)
    podcasts = models.ManyToManyField('podcasts.podcast')
    friends = models.ManyToManyField('self')


class PocketCastsSettings(models.Model):
    email = models.TextField(max_length=256, blank=True, null=True)
    password = models.CharField(max_length=256, blank=True, null=True)
    profile = models.ForeignKey('profiles.profile', related_name='pocketcasts_settings',
                                on_delete=models.DO_NOTHING, default=None, null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
