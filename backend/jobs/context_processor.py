from jobs.models import SiteSetting
from django.shortcuts import render,redirect


def site_setting(request):
    settings = SiteSetting.objects.all().order_by('-created')[0:1]
    
    return {'settings':settings}