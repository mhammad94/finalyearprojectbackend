from django.contrib import admin
from django.contrib.auth.models import User

from apps.users_app.models import CustomUser


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = CustomUser


admin.site.register(CustomUser, UserAdmin)
