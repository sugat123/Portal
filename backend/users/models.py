from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
import random
from django.utils.crypto import get_random_string

TYPES = [
    ('Employeer', 'Employeer'),
    ('Job Seeker', 'Job Seeker')
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.IntegerField(null=False, blank=False, unique=True)
    user_type = models.CharField(max_length=15, choices=TYPES, default='Job Seeker')

    def __str__(self):
        return '{}'.format(self.user.username)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# post_save.connect(create_user_profile, sender=User,
#                   dispatch_uid="users_signal")
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


def generate_activation_code():
    return (get_random_string(6, allowed_chars='0123456789'))

class ActivationCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)
    code = models.CharField(max_length=6, default=generate_activation_code)





