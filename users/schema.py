from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        # only_fields = ('id', 'email', 'password', 'username')


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(username=username, password=password, email=email)
        user.set_password(password)
        user.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    user_by_name = graphene.Field(UserType, username = graphene.String(required=True))
    me = graphene.Field(UserType)

    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

    def resolve_user_by_name(self, info, username):
        return get_user_model().objects.get(username=username)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Not logged in!')
        return user
