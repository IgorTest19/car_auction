from django.contrib import admin
from .models import UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']