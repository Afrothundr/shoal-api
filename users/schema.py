import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .mutations import CreateUser, SaveUser, AddFriend, RemoveFriend, FollowPodcast, UnfollowPodcast, CreatePocketCastSettings
from .types import UserType
from django.db.models import Q, F
from django.db.models import Value as V
from django.db.models.functions import Concat


class Query(graphene.ObjectType):
    users = graphene.List(UserType, search_query=graphene.String())
    me = graphene.Field(UserType)
    is_username_available = graphene.Boolean(username=graphene.String())
    is_email_available = graphene.Boolean(email=graphene.String())

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user

    def resolve_users(self, info, **kwargs):
        search_query = kwargs.get('search_query', None)
        if search_query:
            return get_user_model().objects.annotate(
                full_name=Concat('first_name', V(' '), 'last_name')
            ).filter(
                Q(full_name__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
        else:
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
    create_pocketcast_settings = CreatePocketCastSettings.Field()
