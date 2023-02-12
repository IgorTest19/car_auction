from django.contrib import admin

from .models import Car, CarImage


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """Car class representation in the admin interface."""
    list_display = ['id', 'owner', 'brand', 'model', 'year', 'publish', 'created', 'update']


@admin.register(CarImage)
class CarImage(admin.ModelAdmin):
    """Image class representation in the admin interface."""
    list_display = ['image_id', 'car_id', 'car', 'image']

    def image_id(self, obj):
        """Returning Car's ID to display it alongside with other Car's fields."""
        return obj.id

    image_id.short_description = 'image id'
