import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from podcasts.models import Podcast
from django.db import IntegrityError
from cryptography.fernet import Fernet
from api.settings import FERNET_KEY
from profiles.models import PocketCastsSettings
from profiles.schema import PocketCastsSettingsType
from .types import UserType


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        firstName = graphene.String(required=True)
        lastName = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, firstName, lastName, password, email):
        user = get_user_model()(
            username=username,
            email=email,
            first_name=firstName,
            last_name=lastName
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class SaveUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        firstName = graphene.String(required=True)
        lastName = graphene.String(required=True)
        bio = graphene.String(required=True)

    def mutate(self, info, firstName, lastName, bio):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        user.first_name = firstName
        user.last_name = lastName
        user.profile.bio = bio

        user.save()

        return SaveUser(user=user)

class CreatePocketCastSettings(graphene.Mutation):
    setting = graphene.Field(PocketCastsSettingsType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        user.profile.pocketcasts_settings.all().delete()
        
        setting = PocketCastsSettings(
            email=email,
            password=Fernet(FERNET_KEY).encrypt(password.encode()),
            profile=user.profile 
        )
        setting.save()

        return CreatePocketCastSettings(setting=setting)


class AddFriend(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        friend = get_user_model().objects.get(id=id)

        user.profile.friends.add(friend.profile)

        user.save()

        return AddFriend(user=user)


class RemoveFriend(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        friend = get_user_model().objects.get(id=id)

        user.profile.friends.remove(friend.profile)

        user.save()

        return RemoveFriend(user=user)


class FollowPodcast(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        podcast_id = graphene.ID(required=True)
    
    def mutate(self, info, podcast_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        try:
            podcast = Podcast(
              podcast_id = podcast_id
            )
            podcast.save()

            user.profile.podcasts.add(podcast)

            user.save()

            return FollowPodcast(user=user)

        except IntegrityError:
            print('dupe')
            podcast = Podcast.objects.get(podcast_id=podcast_id)

            user.profile.podcasts.add(podcast)

            user.save()

            return FollowPodcast(user=user)
        pass

class UnfollowPodcast(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        podcast_id = graphene.ID(required=True)
    
    def mutate(self, info, podcast_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        podcast = Podcast.objects.get(podcast_id=podcast_id)

        user.profile.podcasts.remove(podcast)

        user.save()

        return UnfollowPodcast(user=user)

