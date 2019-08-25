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
    commission = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class Skills(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique_with='id', populate_from='title')
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=100, blank=True, null=True)

    def __str__(self):
        return "{0}'s Skill: {1}".format(self.job_type, self.title)

    class Meta:
        verbose_name_plural = 'Skill'


class Facility(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique_with='id', populate_from='title')
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)

    title = models.CharField(
        max_length=100, blank=True, null=True)

    def __str__(self):
        return "{0}'s Facility: {1}".format(self.job_type, self.title)

    class Meta:
        verbose_name_plural = 'Facility'


class PostedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    experience = models.IntegerField(blank=True, null=True)
    skills = models.ManyToManyField(Skills, blank=True)
    facility = models.ManyToManyField(Facility, blank=True)
    salary = models.IntegerField(blank=True, null=True)
    working_time = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique_with='id', populate_from='user')

    def __str__(self):
        return "Job Posted for: {}".format(self.job_type)

    def get_skills(self):
        return "\n, ".join([s.title for s in self.skills.all()])

    def get_facility(self):
        return "\n, ".join([f.title for f in self.facility.all()])


class AppliedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    experience = models.IntegerField(null=True, blank=True)
    skills = models.ManyToManyField(Skills, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique_with='id', populate_from='user')

    def __str__(self):
        return "Job Applied by: {}".format(self.user)

    def get_skills(self):
        return "\n, ".join([s.title for s in self.skills.all()])


class SiteSetting(models.Model):
    logo = models.ImageField(upload_to='setting',)
    about_text = models.TextField()
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class Banner(models.Model):
    index = models.ImageField(upload_to='banner', default='default.jpg')
    login_register = models.ImageField(
        upload_to='banner', default='default.jpg')
    dashboard = models.ImageField(upload_to='banner', default='default.jpg')
    newsfeed = models.ImageField(upload_to="banner", default='default.jpg')
    newsfeed_detail = models.ImageField(
        upload_to="banner", default='default.jpg')
    job = models.ImageField(upload_to="banner", default='default.jpg')
    app = models.ImageField(upload_to="banner", default='default.jpg')
    app_bg = models.ImageField(upload_to="banner", default='default.jpg')
    created = models.DateTimeField(auto_now_add=True)


class Match(models.Model):
    posted_id = models.IntegerField()
    applied_id = models.IntegerField()
    score = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    profile_id = models.IntegerField()
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=200)
    product = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    created_on = models.DateTimeField()
