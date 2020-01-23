import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.db import IntegrityError
from django.db.models import Q

from users.schema import UserType
from api.utilities import Utilities
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


class Query(graphene.ObjectType):
    podcasts = graphene.List(PodcastType)

    comments = graphene.List(
        CommentType,
        podcastId=graphene.ID()
    )

    likes = graphene.List(LikeType)

    best_podcasts = graphene.JSONString()

    fetch_podcast = graphene.JSONString(podcastId=graphene.ID())

    def resolve_podcasts(self, info, **kwargs):
        return Podcast.objects.all()

    def resolve_comments(self, info, podcastId, **kwargs):
        podcast = Podcast.objects.get(podcast_id=podcastId)
        return Comment.objects.filter(podcast=podcast)

    def resolve_best_podcasts(self, info, **kwargs):
        util = Utilities()
        response = util.api_request(path='/best_podcasts?page=1&region=us')
        return response.json()
    
    def resolve_fetch_podcast(self, info, podcastId, **kwargs):
        util = Utilities()
        response = util.api_request(path='/podcasts/' + podcastId)
        return response.json()
    
    def resolve_likes(self, info, **kwargs):
        return Like.objects.all()


class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        podcast_id = graphene.ID()
        body = graphene.String()

    def mutate(self, info, podcast_id, body):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in to post a comment')
        
        podcast = Podcast.objects.get(podcast_id=podcast_id)
        comment = Comment(
            podcast=podcast,
            body=body,
            posted_by=user
        )

        comment.save()

        return CreateComment(comment=comment)

class RemoveComment(graphene.Mutation):
    podcast = graphene.Field(PodcastType)

    class Arguments:
        podcast_id = graphene.ID()
        comment_id = graphene.ID()

    def mutate(self, info, podcast_id, comment_id):

        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in to remove a comment')

        podcast = Podcast.objects.get(podcast_id=podcast_id)

        podcast.comments.filter(id=comment_id).delete()
        podcast.save()

        return RemoveComment(podcast=podcast)

class CreateLike(graphene.Mutation):
    like = graphene.Field(LikeType)

    class Arguments:
        podcast_id = graphene.ID()
        comment_id = graphene.ID()

    def mutate(self, info, **kwargs):
        podcast_id = kwargs.get('podcast_id', 0)
        comment_id = kwargs.get('comment_id', 0)

        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in to like something')
        
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            comment = None

        try: 
            podcast = Podcast.objects.get(podcast_id=podcast_id)
        except Podcast.DoesNotExist:
            podcast = None

        like = Like(
            podcast=podcast,
            comment=comment,
            posted_by=user
        )


        like.save()
        return CreateLike(like=like)

class RemoveLike(graphene.Mutation):
    podcastOrComment = graphene.Field(PodcastOrCommentType)

    class Arguments:
        podcast_id = graphene.ID()
        comment_id = graphene.ID()
        like_id = graphene.ID()

    def mutate(self, info, like_id, **kwargs):
        podcast_id = kwargs.get('podcast_id', None)
        comment_id = kwargs.get('comment_id', None)

        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in to unlike something')

        like = Like.objects.get(id=like_id)

        if comment_id:
            comment = Comment.objects.get(id=comment_id)
            comment.likes.remove(like)
            comment.save()

            return RemoveLike(podcastOrComment=comment)

        if podcast_id:
            podcast = Podcast.objects.get(podcast_id=podcast_id)
            podcast.likes.remove(like)
            podcast.save()

            return RemoveLike(podcastOrComment=podcast)

class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    create_like = CreateLike.Field()
    remove_like = RemoveLike.Field()
    remove_comment = RemoveComment.Field()
