import graphene
import requests
import os
import environ
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.db import IntegrityError
from django.db.models import Q

from users.schema import UserType
from .models import Podcast, Comment


class PodcastType(DjangoObjectType):
    class Meta:
        model = Podcast


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class Query(graphene.ObjectType):
    podcasts = graphene.List(PodcastType)

    comments = graphene.List(
        CommentType,
        podcastId=graphene.ID()
    )

    best_podcasts = graphene.JSONString()

    def resolve_podcasts(self, info, **kwargs):
        return Podcast.objects.all()

    def resolve_comments(self, info, podcastId, **kwargs):
        return Comment.objects.filter(podcast_id=podcastId)

    def resolve_best_podcasts(self, info, **kwargs):

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_file = os.path.join(BASE_DIR, '.env')

        env = environ.Env()
        # reading .env file
        environ.Env.read_env(env_file)
        url = env('API_BASE_URL') + '/best_podcasts?page=1&region=us'
        headers = {
            'X-ListenAPI-Key': env('API_KEY'),
        }
        response = requests.request('GET', url, headers=headers)

        return response.json()


class CreateComment(graphene.Mutation):
    podcast_id = graphene.ID()
    body = graphene.String()
    date = graphene.DateTime()
    posted_by = graphene.Field(UserType)

    class Arguments:
        podcast_id = graphene.ID()
        body = graphene.String()

    def mutate(self, info, podcast_id, body):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in to post a comment')

        comment = Comment(
            podcast_id=podcast_id,
            body=body,
            posted_by=user
        )

        comment.save()

        return CreateComment(comment=comment)


class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
