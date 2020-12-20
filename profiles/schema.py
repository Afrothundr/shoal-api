import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .models import Profile, PocketCastsSettings


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile

class PocketCastsSettingsType(DjangoObjectType):
    class Meta:
        model = PocketCastsSettings


