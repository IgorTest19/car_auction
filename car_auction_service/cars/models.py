from django.db import models
from django.conf import settings

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
    brand = models.CharField(max_length=250, default='Brand like Volvo')
    model = models.CharField(max_length=250, default='Model like V60')

    class Meta:
        verbose_name = 'car'
        verbose_name_plural = 'cars'

    def __str__(self):
        return f'{self.brand} {self.model}'
