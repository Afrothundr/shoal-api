import graphene
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

    def resolve_podcasts(self, info, **kwargs):
        return Podcast.objects.all()

    def resolve_comments(self, info, podcastId, **kwargs):
        return Comment.objects.filter(podcast=podcastId)


class CreatePodcast(graphene.Mutation):
    id = graphene.ID()
    title = graphene.String()
    author = graphene.String()
    description = graphene.String()
    url = graphene.String()
    episodesSortOrder = graphene.Int()
    language = graphene.String()
    categories = graphene.List(graphene.String)
    thumbnailurl = graphene.String()
    thumbnailSmall = graphene.String()
    mediatype = graphene.String()

    class Arguments:
        title = graphene.String()
        author = graphene.String()
        description = graphene.String()
        url = graphene.String()
        episodesSortOrder = graphene.Int()
        language = graphene.String()
        categories = graphene.List(graphene.String)
        thumbnailurl = graphene.String()
        thumbnailSmall = graphene.String()
        mediatype = graphene.String()

    def mutate(self, info, **kwargs):
        podcast = Podcast(
            title=kwargs.get('title'),
            author=kwargs.get('author'),
            description=kwargs.get('description'),
            url=kwargs.get('url'),
            episodesSortOrder=kwargs.get('episodesSortOrder'),
            language=kwargs.get('language'),
            categories=kwargs.get('categories'),
            thumbnailurl=kwargs.get('thumbnailurl'),
            thumbnailSmall=kwargs.get('thumbnailSmall'),
            mediatype=kwargs.get('mediatype')
        )

        try:
            podcast.save()
        except IntegrityError:
            print('dupe')
            pass

        return CreatePodcast(
            id=podcast.id,
            title=podcast.title,
            author=podcast.author,
            description=podcast.description,
            url=podcast.url,
            episodesSortOrder=podcast.episodesSortOrder,
            language=podcast.language,
            categories=podcast.categories,
            thumbnailurl=podcast.thumbnailurl,
            thumbnailSmall=podcast.thumbnailSmall,
            mediatype=podcast.mediatype
        )


class CreateComment(graphene.Mutation):
    id = graphene.ID()
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

        podcast = Podcast.objects.filter(id=podcast_id).first()
        if not podcast:
            raise GraphQLError('Invalid Podcast')

        comment = Comment(
            body=body,
            posted_by=user,
            podcast=podcast
        )

        comment.save()

        return CreateComment(
            id=comment.id,
            body=comment.body,
            date=comment.date,
            posted_by=comment.posted_by
        )


class Mutation(graphene.ObjectType):
    create_podcast = CreatePodcast.Field(),
    create_comment = CreateComment.Field()
