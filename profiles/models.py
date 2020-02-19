from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=256, blank=True)
    podcasts = models.ManyToManyField('podcasts.podcast') 
    friends = models.ManyToManyField('self')
    pocketCastsSettings = models.OneToOneField(PocketCastsSettings, on_delete=models.CASCADE)

class PocketCastsSettings(model.Model):
    usesPocketCasts: models.BooleanField(default=False)
    email: models.TextField(max_length=256, blank=True)
    password: models.CharField(max_length=256, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()