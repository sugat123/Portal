from jobs.models import SiteSetting, Banner, Match, PostedJob, AppliedJob
from django.shortcuts import render, redirect


def site_setting(request):
    settings = SiteSetting.objects.all().order_by('-created')[0:1]

    return {'settings': settings}


def banner(request):
    banners = Banner.objects.all().order_by('-created')[0:1]

    return {'banners': banners}


def notification(request):
    matches = Match.objects.all()
    posted = PostedJob.objects.all()
    applied = AppliedJob.objects.all()

    return {'matches': matches, 'posted': posted, 'applied': applied}
