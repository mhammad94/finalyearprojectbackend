import graphene

from apps.topics_app.schema import TopicsMuations, TopicQuery
from apps.users_app.schema import UserMutations, UserQuery


class Mutations(UserMutations,TopicsMuations, graphene.ObjectType):
    pass


class Query(UserQuery, TopicQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query,mutation=Mutations)