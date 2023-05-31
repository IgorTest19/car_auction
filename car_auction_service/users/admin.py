from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
