from django.db import models
from autoslug import AutoSlugField

class JobType(models.Model):
    title = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique_with='id', populate_from='title')

    def __str__(self):
        return self.title




