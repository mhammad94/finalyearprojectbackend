from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import login,logout
from apps.users_app.models import CustomUser
from graphql_jwt.shortcuts import get_token

class AuthBackend(ModelBackend):
    def authenticate(self, request,username=None, email=None, password=None, **kwargs):

        user_name = kwargs.get("username", None)
        if user_name is not None:
            user = CustomUser.objects.get(username=user_name)
            return user

        if email and password:
            user = CustomUser.objects.filter(email=email)
            if user:
                user = user.first()


                if user.is_approved == False:
                    raise Exception("You are not approved please contact your Administrator")


                if user.is_user_banned == True:
                    raise Exception("You have been banned, please contact your Administrator")


                if user.check_password(password):
                    login(request, user, 'authbackend')
                    return user
                else:
                    raise Exception("Invalid password")

            else:
                raise Exception("Email or password is incorrect")