from django.conf import settings
from django.db import models
from django.utils import timezone


class Car(models.Model):
    """
    Stores a single car. Related to:
    :model: 'auth.User'
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='car_owner') # modify relation to onetoone field
    users_observing = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name='car_observer', blank=True)
    brand = models.CharField(max_length=250, blank=False, null=False)
    model = models.CharField(max_length=250, blank=False, null=False)
    year = models.IntegerField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    valid = models.BooleanField(default=True)
    location = models.CharField(max_length=250, blank=True, null=True)


    class Meta:
        """Metadata class."""
        verbose_name = 'car'
        verbose_name_plural = 'cars'
        ordering = ('-publish',)

    def __str__(self):
        """String representation of the car class object."""
        return f'{self.brand} {self.model}'

    def get_image(self):
        """
        Get the url of image
        :return: value of photo filed in url from.
        :rtype: str
        """
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return None

    def get_first_image(self):
        """
        Get the first image of specified car's image set.
        :return: url of the first image.
        :rtype: str
        """
        first_image = (self.carimage_set.all()[::-1])[0]
        if first_image.image and hasattr(first_image.image, 'url'):
            return first_image.image.url
        else:
            return None

    def get_all_images(self):
        """
        Get all the images of specified car
        :return: set of CarImage objects.
        :rtype: set
        """
        return self.carimage_set.all()

    def observers(self):
        """
        Show users observing this car
        :return:
        :rtype:
        """
        return ','.join([str(user) for user in self.users_observing.all()])


class CarImage(models.Model):
    """
    Image class for Car class. Related to:
    :model: 'cars.Car'
    """
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def get_image(self):
        """
        Get the image.
        :return: url of the image
        :rtype: str
        """
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return None
