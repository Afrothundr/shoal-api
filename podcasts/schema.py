import graphene
from graphene_django import DjangoObjectType
from django.db import IntegrityError

from .models import Podcast


class PodcastType(DjangoObjectType):
    class Meta:
        model = Podcast


class Query(graphene.ObjectType):
    podcasts = graphene.List(PodcastType)

    def resolve_podcasts(self, info, **kwargs):
        return Podcast.objects.all()


class CreatePodcast(graphene.Mutation):
    id = graphene.Int()
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
class Mutation(graphene.ObjectType):
    create_podcast = CreatePodcast.Field()