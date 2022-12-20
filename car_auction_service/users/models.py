from django.db import models
from cars.models import Car
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# https://stackoverflow.com/questions/58794639/how-to-make-follower-following-system-with-django-model
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
# https://www.youtube.com/watch?v=1tZg5YLsCO4&ab_channel=Pyplane

# utworzyć model użytkownica rozszerzająćy domyślny mdoel i dać onetoonefiled z Carmodel

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cars_observed = models.ManyToManyField(Car, related_name='cars_observed', blank=True)

    def __str__(self):
        return str(self.user.username)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()