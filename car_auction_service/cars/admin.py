from django.contrib import admin
from .models import Car, Image

# Register your models here.

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'brand', 'model', 'year', 'publish', 'created', 'update', 'photo']

# admin.site.register(Car)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['car', 'image']
