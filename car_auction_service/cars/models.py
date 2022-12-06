from django.db import models
from django.conf import settings

from django.utils import timezone
# Create your models here.


class Car(models.Model):

    # BRAND_CHOICES = (
    #     ('audi', 'Audi'),
    #     ('bmw', 'BMW'),
    #     ('volvo', 'Volvo'),
    #     ('volkswagen', 'Volkswagen'),
    # )
    #
    # MODEL_CHOICES = (
    #     ('cc', 'CC'),
    #     ('v60', 'V60'),
    #     ('3 series', '3 Series'),
    # )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    brand = models.CharField(max_length=250, blank=False, null=False)
    model = models.CharField(max_length=250, blank=False, null=False)
    year = models.IntegerField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    valid = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'car'
        verbose_name_plural = 'cars'
        ordering = ('-publish',)

    def __str__(self):
        return f'{self.brand} {self.model}'

    def get_image(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return None


class Image(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)