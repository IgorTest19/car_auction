from django.contrib import admin
from .models import Car

# Register your models here.

@admin.register
class CarAdmin(Car):
    list_display = ['owner', 'brand', 'model', 'year', 'publish', 'created', 'update', 'photo']

# admin.site.register(Car)
