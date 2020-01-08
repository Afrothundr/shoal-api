import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .mutations import CreateUser, SaveUser, AddFriend, RemoveFriend, FollowPodcast, UnfollowPodcast
from .types import UserType

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user

    def resolve_users(self, info):
        return get_user_model().objects.all()


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    save_user = SaveUser.Field()
    add_friend = AddFriend.Field()
    remove_friend = RemoveFriend.Field()
    follow_podcast = FollowPodcast.Field()
    unfollow_podcast = UnfollowPodcast.Field()
