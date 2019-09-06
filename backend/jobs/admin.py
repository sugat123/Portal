from django.contrib import admin
from .models import *
from django.core.mail import send_mail


@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('title',)
    search_fields = ('title',)


@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ('title', 'job_type')
    ordering = ('title',)
    search_fields = ('title', 'job_type__title')
    list_filter = ('job_type__title',)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('title', 'job_type')
    ordering = ('title',)
    search_fields = ('title', 'job_type__title')
    list_filter = ('job_type__title',)


@admin.register(PostedJob)
class PostedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_type', 'experience', 'get_skills',
                    'get_facility', 'salary', 'working_time', 'location')
    ordering = ('user',)
    search_fields = ('job_type__title', 'user')
    list_filter = ('created', 'job_type', )


@admin.register(AppliedJob)
class AppliedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_type', 'experience', 'get_skills', 'location')
    ordering = ('user',)
    search_fields = ('job_type__title', 'user')
    list_filter = ('created', 'job_type', )


admin.site.register(SiteSetting)
admin.site.register(Banner)
admin.site.register(Payment)
admin.site.register(Verification)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'posted_id', 'applied_id', 'score']
    ordering = ('created', )


    

