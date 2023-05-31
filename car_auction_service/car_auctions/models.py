from django.conf import settings
from django.db import models
from django.utils import timezone


class CarAdvert(models.Model):
    """
    Stores a single caradvert. Related to:
    :model: 'auth.User'
    """

    CURRENCY_CHOICES = (("pln", "PLN"), ("eur", "EURO"))
    PRICE_TYPE_CHOICES = (("gross", "GROSS"), ("net", "NET"))
    FUEL_TYPE_CHOICES = (
        ("petrol", "Petrol"),
        ("diesel", "Diesel"),
        ("hybrid_petrol", "Hybrid (petrol/electric)"),
        ("hybrid_diesel", "Hybrid (diesel/electric)"),
        ("hybrid_plug_in", "Hybrid-plug-in"),
        ("electric", "Electric"),
        ("petrol_lpg", "Petrol-LPG"),
        ("petrol_lng", "Petrol-LNG"),
        ("hydrogen", "Hydrogen"),
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="car_ad_owner")
    users_observing = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name="car_ad_observer", blank=True)
    brand = models.CharField(max_length=250, blank=False, null=False)
    model = models.CharField(max_length=250, blank=False, null=False)
    engine_capacity = models.FloatField(blank=True, null=True)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, blank=True, null=True, default="petrol")
    year = models.IntegerField()
    location = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default="pln")
    price_type = models.CharField(max_length=10, choices=PRICE_TYPE_CHOICES, default="gross")
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    is_valid = models.BooleanField(default=True, null=False)

    class Meta:
        """Metadata class."""

        verbose_name = "car advertisement"
        verbose_name_plural = "car advertisements"
        ordering = ["-published"]

    def __str__(self):
        """String representation of the caradvert class object."""
        # return f'{self.brand} {self.model}'
        return f"{self.id}"

    def get_image(self):
        """
        Get the url of image
        :return: value of photo filed in url from.
        :rtype: str
        """
        if self.photo and hasattr(self.photo, "url"):
            return self.photo.url
        else:
            return None

    def get_first_image(self):
        """
        Get the first image of specified caradvert's image set.
        :return url of the first image.
        :rtype: str
        """

        if len(self.carimage_set.all()) != 0:
            first_image = self.carimage_set.first()
        else:
            return None
        if first_image.image and hasattr(first_image.image, "url"):
            return first_image.image.url
        else:
            return None

    def get_all_images(self):
        """
        Get all the images of specified caradvert
        :return: set of CarImage objects.
        :rtype: set
        """
        # return self.carimage_set.all()
        return self.carimage_set.all()

    def observers(self):
        """
        Show users observing this caradvert,
        :return:
        :rtype:
        """
        return ",".join([str(user) for user in self.users_observing.all()])


class CarImage(models.Model):
    """
    Image class for CarAd class. Related to:
    :model: 'car_auctions.CarAdvert'
    """

    car_advert = models.ForeignKey(CarAdvert, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", default="images/no_car_image.png", blank=True, null=True)

    def get_image(self):
        """
        Get the image.
        :return: url of the image
        :rtype: str
        """
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        else:
            return None


class RecentlyViewed(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_viewed")
    car_advert = models.ForeignKey(CarAdvert, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
