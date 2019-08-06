from django.db import models
from autoslug import AutoSlugField
from users.models import *
from django.contrib.auth.models import User


class JobType(models.Model):
    title = models.CharField(max_length=25, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    icon = models.CharField(max_length=50, blank=True,
                            null=True, default='fas fa-briefcase')
    slug = AutoSlugField(unique_with='id', populate_from='title')

    def __str__(self):
        return self.title


class Skills(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique_with='id', populate_from='title')
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{0}'s Skill: {1}".format(self.job_type, self.title)

    class Meta:
        verbose_name_plural = 'Skill'


class Facility(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique_with='id', populate_from='title')
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)

    title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{0}'s Facility: {1}".format(self.job_type, self.title)

    class Meta:
        verbose_name_plural = 'Facility'


class PostedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    experience = models.IntegerField(blank=True, null=True)
    skills = models.ManyToManyField(Skills, blank=True, null=True)
    facility = models.ManyToManyField(Facility, blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    working_time = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "Job Posted for: {}".format(self.job_type)


class AppliedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    experience = models.IntegerField(null=True, blank=True)
    skills = models.ManyToManyField(Skills, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "Job Applied by: {}".format(self.user)
