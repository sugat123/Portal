from django.db import models
from autoslug import AutoSlugField
from users.models import *
from django.contrib.auth.models import User


class JobType(models.Model):
    title = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
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


class Facility(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique_with='id', populate_from='title')
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{0}'s Facility: {1}".format(self.job_type, self.title)


class Experience(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique_with='id', populate_from='years')
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    years = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return "{0}: {1} years".format(self.job_type, self.years)


class PostedJob(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    job_type = models.ForeignKey(JobType, on_delete=models.PROTECT)
    experience = models.ForeignKey(Experience, on_delete=models.PROTECT)
    skills = models.ForeignKey(Skills, on_delete=models.PROTECT)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)

    def __str__(self):
        return "Job Posted for: {}".format(self.job_type)


class AppliedJob(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    job_type = models.ForeignKey(JobType, on_delete=models.PROTECT)
    experience = models.ForeignKey(Experience, on_delete=models.PROTECT)
    skills = models.ForeignKey(Skills, on_delete=models.PROTECT)

    def __str__(self):
        return "Job Applied by: {}".format(self.user)
