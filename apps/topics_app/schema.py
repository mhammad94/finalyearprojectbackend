import graphene
from graphene import String
from graphene_django import DjangoObjectType

from apps.topics_app.models import ForumTopic, Comment, FilterKeywords


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


class FilterKeywordsType(DjangoObjectType):
    class Meta:
        model = FilterKeywords

class TopicsOutput(graphene.ObjectType):
    ok = graphene.Boolean()
    errors = graphene.String()
    success_message = graphene.String()
    topics = graphene.List(TopicType)
    filter_keywords = graphene.List(String)


class FilterKeywordsQuery(graphene.ObjectType):
    ok = graphene.Boolean()
    errors = graphene.String()
    success_message = graphene.String()
    filter_keywords = graphene.List(FilterKeywordsType)



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

class AddKeyword(graphene.Mutation):
    class Arguments:
        keyword = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.String()
    success_message = graphene.String()

    def mutate(self, info, keyword):

        try:
            create_keyword_query = FilterKeywords.objects.create(key_word=keyword)
            create_keyword_query.save()
            return AddKeyword(ok=True, errors="", success_message="Keyword Added Successfully")
        except Exception as e:
            return AddKeyword(ok=True, errors=str(e), success_message="")


class DeleteKeyword(graphene.Mutation):

    class Arguments:
        keyword_id = graphene.UUID(required=True)

    ok = graphene.Boolean()
    errors = graphene.String()
    success_message = graphene.String()


    def mutate(self, info, keyword_id):

        try:
            key_word_query = FilterKeywords.objects.filter(id=keyword_id)

            if key_word_query.exists():
                key_word_query = key_word_query.first()
                key_word_query.delete()
                return DeleteKeyword(ok=True, errors="", success_message="Keyword deleted successfully")
            else:
                raise Exception("Keyword not found")

        except Exception as e:
            return DeleteKeyword(ok=False, errors=str(e), success_message="")


class TopicQuery(graphene.ObjectType):
    get_all_topics = graphene.Field(TopicsOutput)
    get_all_filter_keywords = graphene.Field(FilterKeywordsQuery)
    def resolve_get_all_topics(self, info, **kwargs):
        try:
           topics_query =  ForumTopic.objects.all()
           filter_keywords_query = FilterKeywords.objects.all()
           filter_keywords = list()
           topics_query = sorted(topics_query, key=lambda x: x.created_at, reverse=True)

           for filter_keyword in filter_keywords_query:
               filter_keywords.append(filter_keyword.key_word)
           response = {
               "ok":True,
               "success_message":"Topic Fetched Successfully",
               "errors":"",
               "topics": topics_query,
               "filter_keywords":filter_keywords
           }
           return response
        except Exception as e:
            response = {
                "ok": False,
                "success_message": "",
                "errors": str(e),
                "topics": [],
                "filter_keywords":[]
            }
            return response


    def resolve_get_all_filter_keywords(self, info):
        try:
            filter_keywords_query = FilterKeywords.objects.all()
            filter_keywords_query = sorted(filter_keywords_query, key=lambda x: x.created_at, reverse=True)

            response = {
                "ok":True,
                "errors":"",
                "success_message":"Fetched Filter Keywords",
                "filter_keywords": filter_keywords_query
            }
            return response
        except Exception as e:
            response = {
                "ok": True,
                "errors": "",
                "success_message": "Fetched Filter Keywords",
                "filter_keywords": []
            }
            return response

class TopicsMuations(graphene.ObjectType):
      add_new_topic = AddNewTopic.Field()
      add_new_comment = AddNewComment.Field()
      delete_comment = DeleteComment.Field()
      delete_topic = DeleteTopic.Field()
      add_key_word = AddKeyword.Field()
      delete_key_word = DeleteKeyword.Field()
