from django.contrib import admin
from .models import Car, CarImage

# Register your models here.

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'brand', 'model', 'year', 'publish', 'created', 'update']

# admin.site.register(Car)

@admin.register(CarImage)
class CarImage(admin.ModelAdmin):
    # class Meta:
    #     model = CarImage
    #     fields = ['image_id', 'car_id', 'car', 'image']

    list_display = ['image_id', 'car_id', 'car', 'image']

    def image_id(self, obj):
        return obj.id

    image_id.short_description = 'image id'



