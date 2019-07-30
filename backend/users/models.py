from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

user_types= ['seeker', 'giver']
TYPES = (
    (user_types[0], 'seeker'),
    (user_types[1], 'giver')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    user_type = models.CharField(max_length=15, choices=TYPES)

    def __str__(self):
        return '{}'.format(self.user.username)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# post_save.connect(create_user_profile, sender=User,
#                   dispatch_uid="users_signal")


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
