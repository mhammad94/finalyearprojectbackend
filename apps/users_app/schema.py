import graphene
import graphql_jwt
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from django.contrib.auth import login
from apps.users_app.models import CustomUser, UserRoleRoutes
from graphql_jwt.shortcuts import get_token, get_refresh_token
from graphql_jwt.decorators import login_required, jwt_cookie
from django.contrib.auth import authenticate, login, logout

from decorators.decorators import login_required_custom


class UserRoleType(DjangoObjectType):
    class Meta:
        model = UserRoleRoutes

class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser

    user_type_display = graphene.String()
    user_routes = graphene.List(UserRoleType)

    def resolve_user_type_display(self,info):
        value_mapping = {
            0:'Admin',
            1:'Moderator',
            2:'Normal User'
        }
        return value_mapping.get(self.user_type, "Unknown Value")

    def resolve_user_routes(self, info):
        return UserRoleRoutes.objects.filter(user_type=self.user_type)



class UserTypeOutput(graphene.ObjectType):
      ok = graphene.Boolean()
      errors = graphene.String()
      users = graphene.List(UserType)


class UserQuery(graphene.ObjectType):
    get_users_for_approval = graphene.Field(UserTypeOutput)
    get_normal_users = graphene.Field(UserTypeOutput)
    @login_required
    def resolve_get_users_for_approval(self, info, **kwargs):
        try:
            users = CustomUser.objects.filter(is_staff=False, user_type__range=(1,2))
            users = sorted(users, key=lambda x: x.date_joined, reverse=True)
            data = {
                "ok":True,
                "errors":"",
                "users":users
            }
            return data
        except Exception as e:
            data = {
                "ok":False,
                "errors":str(e),
                "users":[]
            }
            return data


    def resolve_get_normal_users(self, info, **kwargs):
        try:
            users = CustomUser.objects.filter(is_staff=False, user_type=2, is_approved=True)
            users = sorted(users, key=lambda x: x.date_joined, reverse=True)
            data = {
                "ok": True,
                "errors": "",
                "users": users
            }
            return data
        except Exception as e:
            data = {
                "ok": False,
                "errors": str(e),
                "users": []
            }
            return data

class Login(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.String()
    token = graphene.String()
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, email, password):

        try:
            user = authenticate(info.context,username="",email=email, password=password)
            if user:
                access_token = get_token(user)
                return Login(ok=True, errors="", token=access_token, user=user)

        except Exception as e:
            return Login(ok=False,
                         errors=str(e),
                         token="",
                         )

class Logout(graphene.Mutation):

    ok = graphene.Boolean()
    errors = graphene.String()
    success_message = graphene.String()


    def mutate(root, info):
        try:
            user = info.context.user
            logout(info.context)
            return Logout(ok=True, errors="", success_message="Logged Out")
        except Exception as e:
            return Logout(ok=False, errors=str(e), success_message="")
class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)
    ok = graphene.Boolean()
    errors = graphene.String()
    success_message = graphene.String()
    @classmethod
    def resolve(cls, root, info, **kwargs):
        try:
            return cls(user=info.context.user, ok=True, errors="", success_message="Logged In")
        except Exception as e:
            return cls(user=[], ok=False, errors=str(e), success_message="")

class SignupNormalUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.String()
    success_message = graphene.String()


    def mutate(root, info, email, password, first_name, last_name):

        try:
            user_email_query = CustomUser.objects.filter(email=email)
            if user_email_query.exists():
                raise Exception("User already exists")
            user = CustomUser.objects.create_user(email=email,
                                                  password=password,
                                                  first_name=first_name,
                                                  last_name=last_name,
                                                  user_type=2,
                                                  username=email)
            user.save()
            return SignupNormalUser(ok=True, errors="", success_message="You have signed up sucessfully, please wait for Admin Approval")
        except Exception as e:
            return SignupNormalUser(ok=False, errors=str(e), success_message="")


class SignupModeratorUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.String()
    success_message = graphene.String()

    @login_required
    def mutate(root, info, email, password, first_name, last_name,):

        try:
            user_email_query = CustomUser.objects.filter(email=email)
            if user_email_query.exists():
                raise Exception("User already exists")
            user = CustomUser.objects.create_user(email=email,
                                                  password=password,
                                                  first_name=first_name,
                                                  last_name=last_name,
                                                  username=email,
                                                  is_approved=True,
                                                  user_type=1
                                                )
            user.save()
            return SignupModeratorUser(ok=True, errors="", success_message="Moderator created successfully")
        except Exception as e:
            return SignupModeratorUser(ok=False, errors=str(e), success_message="")


class ApproveBlockUserMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.UUID(required=True)
        approved = graphene.Boolean(required=True)

    ok = graphene.Boolean()
    errors = graphene.String()
    success_message = graphene.String()


    def mutate(root, info, user_id, approved):
        try:
            user = CustomUser.objects.filter(id=user_id)
            if user.exists():
                user = user.first()
                user.is_approved = approved
                user.save()
                return ApproveBlockUserMutation(ok=True, errors="", success_message="User approved/Block successfully")
            else:
                raise Exception("User does not exist")
        except Exception as e:
            return ApproveBlockUserMutation(ok=False, errors=str(e), suucess_message="")


class BanUser(graphene.Mutation):

    class Arguments:
        user_id = graphene.UUID(required=True)
        is_banned = graphene.Boolean(required=True)
        ban_start_date = graphene.String()
        ban_end_date = graphene.String()
    
    ok = graphene.Boolean()
    errors = graphene.String()
    success_message = graphene.String()

    def mutate(root, info, user_id, is_banned, ban_start_date, ban_end_date):

        try:
            user = CustomUser.objects.filter(id=user_id)

            if user.exists():
                user = user.first()

                if is_banned and not user.is_user_banned:
                    user.is_user_banned = is_banned
                    user.ban_start_date = ban_start_date
                    user.ban_end_date = ban_end_date
                    user.save()
                    return BanUser(ok=True, success_message="User Banned Successfully", errors="")
                else:
                    user.is_user_banned = is_banned
                    user.save()
                    return BanUser(ok=True, success_message="User UnBanned Successfully", errors="")
            else:
                raise Exception("User Not Found");

        except Exception as e:
            return BanUser(ok=False, success_message="", errors=str(e))
    







class UserMutations(graphene.ObjectType):
    login = Login.Field()
    obtain_token = ObtainJSONWebToken.Field()
    signup_normal_user = SignupNormalUser.Field()
    signup_moderator_user = SignupModeratorUser.Field()
    approve_block_user = ApproveBlockUserMutation.Field()
    ban_user = BanUser.Field()
    logout = Logout.Field()

