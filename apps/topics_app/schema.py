import graphene
from graphene_django import DjangoObjectType

from apps.topics_app.models import ForumTopic, Comment



class CommentsType(DjangoObjectType):
    class Meta:
        model = Comment

class TopicType(DjangoObjectType):
    class Meta:
        model = ForumTopic
    comments = graphene.List(CommentsType)
    comments_count = graphene.Int()

    def resolve_comments(self, info, **kwargs):
        user = info.context.user
        comments_query = Comment.objects.filter(topic_id=self.id)
        return comments_query

    def resolve_comments_count(self, info, **kwargs):
        comments_query = Comment.objects.filter(topic_id=self)
        return comments_query.count()
class TopicsOutput(graphene.ObjectType):
    ok = graphene.Boolean()
    errors = graphene.String()
    success_message = graphene.String()
    topics = graphene.List(TopicType)

class AddNewTopic(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.String()
    success_message = graphene.String()

    def mutate(self, info, title, content):
        print(info.context)
        user = info.context.user
        try:
            new_topic = ForumTopic.objects.create(title=title, content=content, user=user)
            new_topic.save()
            return AddNewTopic(ok=True, errors="", success_message="New Topic Added Successfully")
        except Exception as e:
            return AddNewTopic(ok=False, errors=str(e), success_message="")

class AddNewComment(graphene.Mutation):
    class Arguments:
        content = graphene.String(required=True)
        topic_id = graphene.UUID(required=True)

    ok = graphene.Boolean()
    errors = graphene.String()
    success_message = graphene.String()

    def mutate(self, info, content, topic_id):
        user = info.context.user
        topic_query = ForumTopic.objects.filter(id=topic_id)

        try:
            if topic_query.exists():
                topic_query = topic_query.first()
                new_comment = Comment.objects.create(content=content, topic=topic_query, user=user)
                new_comment.save()
                return AddNewComment(ok=True, errors="", success_message="Comment Added Successfully")
            else:
                raise Exception("No such topic")
        except Exception as e:
            return AddNewComment(ok=False, errors=str(e), success_message="")


class DeleteComment(graphene.Mutation):
    class Arguments:
        comment_id = graphene.UUID(required=True)

    ok = graphene.Boolean()
    errors = graphene.String()
    success_message = graphene.String()

    def mutate(self, info, comment_id):
        comment_query = Comment.objects.filter(id=comment_id)

        try:
            if comment_query.exists():
                comment_query = comment_query.first()
                comment_query.delete()
                return DeleteComment(ok=True, success_message="Comment Deleted")
            else:
                raise Exception("Comment not found")
        except Exception as e:
            return DeleteComment(ok=False, success_message="", errors=str(e))

class DeleteTopic(graphene.Mutation):
    class Arguments:
        topic_id = graphene.UUID(required=True)

    ok = graphene.Boolean()
    errors = graphene.String()
    success_message = graphene.String()

    def mutate(self, info, topic_id):
        topic_query = ForumTopic.objects.filter(id=topic_id)

        try:
            if topic_query.exists():
                topic_query = topic_query.first()
                topic_query.delete()
                return DeleteTopic(ok=True, success_message="Topic Deleted")
            else:
                raise Exception("Topic not found")
        except Exception as e:
            return DeleteTopic(ok=False, success_message="", errors=str(e))
class TopicQuery(graphene.ObjectType):
    get_all_topics = graphene.Field(TopicsOutput)


    def resolve_get_all_topics(self, info, **kwargs):
        try:
           topics_query =  ForumTopic.objects.all()
           response = {
               "ok":True,
               "success_message":"Topic Fetched Successfully",
               "errors":"",
               "topics": topics_query
           }
           return response
        except Exception as e:
            response = {
                "ok": False,
                "success_message": "",
                "errors": str(e),
                "topics": []
            }
            return response


class TopicsMuations(graphene.ObjectType):
      add_new_topic = AddNewTopic.Field()
      add_new_comment = AddNewComment.Field()
      delete_comment = DeleteComment.Field()
      delete_topic = DeleteTopic.Field()
