import graphene
from .types import *
from graphql import GraphQLError
from django.db import IntegrityError
from .models import *

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