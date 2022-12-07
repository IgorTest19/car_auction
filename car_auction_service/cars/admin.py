from django.contrib import admin
from .models import Car, Image

# Register your models here.

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'brand', 'model', 'year', 'publish', 'created', 'update', 'photo']

# admin.site.register(Car)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    class Meta:
        model = Image
        fields = ['image_id', 'car_id', 'car', 'image']
    # list_display = ['image_id', 'car_id', 'car', 'image']
    #
    # def image_id(self, obj):
    #     return obj.id

    # image_id.short_description = 'image id'



