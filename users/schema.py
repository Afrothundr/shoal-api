import graphene
from packages.pcasts import pocketcasts
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from users.mutations import CreateUser, SaveUser, AddFriend, RemoveFriend, FollowPodcast, UnfollowPodcast, CreatePocketCastSettings
from users.types import UserType
from users.models import Episode
from django.db.models import Q, F
from django.db.models import Value as V
from django.db.models.functions import Concat
from cryptography.fernet import Fernet
from api.settings import FERNET_KEY


class Query(graphene.ObjectType):
    users = graphene.List(UserType, search_query=graphene.String())
    me = graphene.Field(UserType)
    is_username_available = graphene.Boolean(username=graphene.String())
    is_email_available = graphene.Boolean(email=graphene.String())
    my_listening_history = graphene.List(Episode)

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

    def resolve_my_listening_history(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        settings = user.profile.pocketcasts_settings.first()
        if not settings:
            raise Exception('Please set PocketCasts settings')

        # Ghetto Byte decoding cause we are saving it wrong
        password = settings.password[2:len(settings.password) - 1]
        pocket = pocketcasts.Pocketcasts(settings.email, password=Fernet(
            FERNET_KEY).decrypt(password.encode()))
        # return jsonpickle.encode(pocket.get_listening_history())
        episodes = pocket.get_listening_history()
        return episodes


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    save_user = SaveUser.Field()
    add_friend = AddFriend.Field()
    remove_friend = RemoveFriend.Field()
    follow_podcast = FollowPodcast.Field()
    unfollow_podcast = UnfollowPodcast.Field()
    create_pocketcast_settings = CreatePocketCastSettings.Field()
