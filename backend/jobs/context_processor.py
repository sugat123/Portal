from jobs.models import SiteSetting,Banner
from django.shortcuts import render,redirect


def site_setting(request):
    settings = SiteSetting.objects.all().order_by('-created')[0:1]
    
    return {'settings':settings}

def banner(request):
    banners = Banner.objects.all().order_by('-created')[0:1]
    
    return {'banners':banners}
