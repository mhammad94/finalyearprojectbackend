import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import datetime, timezone, timedelta
class ForumTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=250, null=False, blank=False, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=False, blank=False, max_length=800)
    user = models.ForeignKey("users_app.CustomUser", on_delete=models.CASCADE, null=False, blank=False)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content = models.TextField(max_length=800, null=False, blank=False)
    user = models.ForeignKey("users_app.CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class FilterKeywords(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    key_word = models.CharField(max_length=250, null=False, blank=False, default="")
    created_at = models.DateTimeField(auto_now_add=True)


