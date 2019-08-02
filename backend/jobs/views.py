from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import *
from .models import *


def index(request):
    profile = Profile.objects.all()
    return render(request, 'jobs/index.html', {'profile': profile})


@login_required
def giver(request):
    job_types = JobType.objects.all()
    return render(request, 'jobs/giver.html', {'job_types': job_types})


@login_required
def seeker(request):
    job_types = JobType.objects.all()
    context = {'job_types': job_types}
    return render(request, 'jobs/seeker.html', context)


@login_required
def add_job(request):
    if request.method == 'POST':
        form = AddJobTypeForm(request.POST or None)
        if form.is_valid():
            form.save()

            return redirect('jobs:add_job')
    else:
        form = AddJobTypeForm()

    return render(request, 'jobs/add_job.html', {'form': form})


@login_required
def post_job(request, slug):
    type = get_object_or_404(JobType, slug=slug)
    skills = Skills.objects.all()
    experiences = Experience.objects.all()
    facilities = Facility.objects.all()
    context = {'type': type,
               'skills': skills,
               'experiences': experiences,
               'facilities': facilities}
    return render(request, 'jobs/post_job.html', context)


@login_required
def list_job(request, slug):
    type = get_object_or_404(JobType, slug=slug)
    posted_jobs = PostedJob.objects.all()
    context = {'posted_jobs': posted_jobs, 'type': type}
    return render(request, 'jobs/list_job.html', context)


@login_required
def add_facility(request):
    if request.method == 'POST':
        form = AddFacilityForm(request.POST or None)
        if form.is_valid():
            form.save()

            return redirect('jobs:add_facility')
    else:
        form = AddFacilityForm()
    return render(request, 'jobs/add_facility.html', {'form': form})


@login_required
def add_skill(request):
    if request.method == 'POST':
        form = AddSkillForm(request.POST or None)
        if form.is_valid():
            form.save()

            return redirect('jobs:add_skill')
    else:
        form = AddSkillForm()

    return render(request, 'jobs/add_skill.html', {'form': form})
