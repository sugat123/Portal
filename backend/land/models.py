from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Facility(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=250, unique=True)

    def __str__(self):

        return("Facility:{}".format(self.title))


class PostedLand(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=50, null=False, blank=False)
    location = models.CharField(max_length=50, null=False, blank=False)
    facility = models.ManyToManyField(Facility)
    price = models.CharField(max_length=100, blank=False, null=False)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return "Posted Land in location {}".format(self.location)

    def get_facility(self):
        return "\n, ".join([f.title for f in self.facility.all()])


def get_image_filename(instance, filename):
    id = instance.posted_land.id
    return "postedland_image/{}".format(id)


class Image(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    posted_land = models.ForeignKey(PostedLand, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              blank=True, null=True)


class SearchedLand(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=50, null=False, blank=False)
    price = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    facility = models.ManyToManyField(Facility)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return "Searched Land in location {}".format(self.location)
