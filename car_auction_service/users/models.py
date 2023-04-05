from django.contrib.auth.models import User
from django.db import models

from cars.models import Car


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cars_observed = models.ManyToManyField(Car, related_name='cars_observed', blank=True)

    def __str__(self):
        return str(self.user.username)

    def cars_observed_by_user(self):
        return ','.join([str(user) for user in self.cars_observed.all()])

    def cars_observed_by_user2(self):
        list1 = [user for user in self.cars_observed.all()]
        return list1