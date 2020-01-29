import graphene
from graphene_django import DjangoObjectType
from api.utilities import Utilities
from .models import Podcast, Comment, Like
from .types import PodcastType, CommentType, LikeType
from .mutations import *

class Query(graphene.ObjectType):
    podcasts = graphene.List(PodcastType)

    comments = graphene.List(
        CommentType,
        podcastId=graphene.ID()
    )

    likes = graphene.List(LikeType)

    best_podcasts = graphene.JSONString(
        genre_id=graphene.ID(),
        page=graphene.ID()
    )

    fetch_podcast = graphene.JSONString(podcastId=graphene.ID())

    fetch_genres = graphene.JSONString()

    def resolve_podcasts(self, info, **kwargs):
        return Podcast.objects.all()

    def resolve_comments(self, info, podcastId, **kwargs):
        podcast = Podcast.objects.get(podcast_id=podcastId)
        return Comment.objects.filter(podcast=podcast)

    def resolve_best_podcasts(self, info, **kwargs):
        genre_id = kwargs.get('genre_id', None)
        page = kwargs.get('page', None)
        util = Utilities()
        response = util.api_request(path=f'/best_podcasts?page={page}&region=us&genre_id={genre_id}')
        return response.json()
    
    def resolve_fetch_podcast(self, info, podcastId, **kwargs):
        util = Utilities()
        response = util.api_request(path='/podcasts/' + podcastId)
        return response.json()
    
    def resolve_likes(self, info, **kwargs):
        return Like.objects.all()
    
    def resolve_fetch_genres(self, info, **kwargs):
        util = Utilities()
        response = util.api_request(path='/genres/')
        return response.json()



class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    create_like = CreateLike.Field()
    remove_like = RemoveLike.Field()
    remove_comment = RemoveComment.Field()
