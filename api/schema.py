import graphene
import graphql_jwt
import users.schema
import podcasts.schema
import profiles.schema



class Query(
        users.schema.Query,
        podcasts.schema.Query,
        graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, podcasts.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)