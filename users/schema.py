import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .mutations import CreateUser, SaveUser, AddFriend, RemoveFriend, FollowPodcast, UnfollowPodcast
from .types import UserType

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    me = graphene.Field(UserType)
    is_username_available = graphene.Boolean(username=graphene.String())
    is_email_available = graphene.Boolean(email=graphene.String())

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_is_username_available(self, info, username):
        userExists = get_user_model().objects.filter(username=username)
        return False if userExists else True

    def resolve_is_email_available(self, info, email):
        userExists = get_user_model().objects.filter(email=email)
        return False if userExists else True
     


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    save_user = SaveUser.Field()
    add_friend = AddFriend.Field()
    remove_friend = RemoveFriend.Field()
    follow_podcast = FollowPodcast.Field()
    unfollow_podcast = UnfollowPodcast.Field()
