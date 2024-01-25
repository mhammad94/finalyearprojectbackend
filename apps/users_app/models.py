from datetime import datetime
import uuid

from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.contrib.auth import authenticate, login


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    is_approved = models.BooleanField(default=False)

    ADMIN = 0
    MODERATOR = 1
    NORMALUSER = 2

    USER_TYPE_CHOICES = (
        (ADMIN, 'Admin')
        , (MODERATOR, 'Moderator')
        , (NORMALUSER, 'Normal User')
    )

    user_type = models.SmallIntegerField(choices=USER_TYPE_CHOICES, default=NORMALUSER)
    is_user_banned = models.BooleanField(default=False)
    ban_start_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    ban_end_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)



class UserRoleRoutes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    route_title = models.CharField(max_length=300, null=True, blank=True)
    route = models.SlugField(max_length=100, null=True, blank=True)
    user_type = models.SmallIntegerField()





