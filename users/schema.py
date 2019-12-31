import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


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


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    save_user = SaveUser.Field()
