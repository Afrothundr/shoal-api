import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .models import Profile


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


