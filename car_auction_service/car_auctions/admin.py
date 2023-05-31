from django.contrib import admin

from .models import CarAdvert, CarImage, RecentlyViewed


@admin.register(CarAdvert)
class CarAdmin(admin.ModelAdmin):
    """Car class representation in the admin interface."""

    list_display = [
        "id",
        "owner",
        "brand",
        "model",
        "year",
        "published",
        "created",
        "updated",
    ]


@admin.register(CarImage)
class CarImage(admin.ModelAdmin):
    """Image class representation in the admin interface."""

    list_display = ["image_id", "car_advert_id", "car_advert", "image"]

    def image_id(self, obj):
        """Returning Car's ID to display it alongside with other Car's fields."""
        return obj.id

    image_id.short_description = "image id"


@admin.register(RecentlyViewed)
class RecentlyViewed(admin.ModelAdmin):
    """Viewed car in history class representation in the admin interface."""

    list_display = ["user", "car_advert", "viewed_at"]
