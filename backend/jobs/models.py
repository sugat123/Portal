from django.db import models
from autoslug import AutoSlugField
from users.models import *
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q


class JobTypeManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(slug__icontains=query)
                         )
            # distinct() is often necessary with Q lookups
            qs = qs.filter(or_lookup).distinct()
        return qs


class JobType(models.Model):
    title = models.CharField(max_length=25, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True,
                              null=True, upload_to='jobtypes')
    slug = AutoSlugField(unique_with='id', populate_from='title')
    commission = models.IntegerField(null=True, blank=True)

    objects = JobTypeManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Job Types'


class Skills(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # slug = AutoSlugField(unique_with='id', populate_from='title')
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=255)

    class Meta:
        unique_together = (("job_type", "title"),)

    def __str__(self):
        return "{0}'s Skill: {1}".format(self.job_type, self.title)


class Facility(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # slug = AutoSlugField(unique_with='id', populate_from='title')
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)

    title = models.CharField(
        max_length=255)

    def __str__(self):
        return "{0}'s Facility: {1}".format(self.job_type, self.title)

    class Meta:
        unique_together = (("job_type", "title"),)
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
    number_of_employee = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique_with='id', populate_from='user')

    def __str__(self):
        return "Job Posted for: {}".format(self.job_type)

    def get_skills(self):
        return "\n, ".join([s.title for s in self.skills.all()])

    def get_facility(self):
        return "\n, ".join([f.title for f in self.facility.all()])

    class Meta:
        verbose_name_plural = 'Posted Jobs'


class AppliedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    experience = models.IntegerField(null=True, blank=True)
    skills = models.ManyToManyField(Skills, blank=True)
    location = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique_with='id', populate_from='user')

    def __str__(self):
        return "Job Applied by: {}".format(self.user)

    def get_skills(self):
        return "\n, ".join([s.title for s in self.skills.all()])

    class Meta:
        verbose_name_plural = 'Applied Jobs'


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
    job_type = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = 'Matched Jobs'


class Payment(models.Model):
    profile_id = models.IntegerField(null=True)
    name = models.CharField(max_length=100, null=True)
    amount = models.IntegerField(null=True)
    product = models.IntegerField(null=True)
    mobile = models.CharField(max_length=20, null=True)
    created_on = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = 'Payments'


class Verification(models.Model):
    payment_id = models.IntegerField()
    user_id = models.IntegerField(null=True)
    paid_status = models.BooleanField(default=False, null=True)
    match_id = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = 'Verified Payments'


class Exchange(models.Model):
    user_id = models.IntegerField()
    match_id = models.IntegerField()
