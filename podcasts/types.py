import graphene
from graphene_django import DjangoObjectType
from .models import Podcast, Comment, Like

class PodcastType(DjangoObjectType):
    class Meta:
        model = Podcast


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class LikeType(DjangoObjectType):
    class Meta:
        model = Like

class PodcastOrCommentType(graphene.Union):
    class Meta:
        types = (PodcastType, CommentType)