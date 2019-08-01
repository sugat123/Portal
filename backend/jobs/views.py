from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import *
from .models import *


def index(request):
    return render(request, 'jobs/base.html')


@login_required
def giver(request):
    job_types = JobType.objects.all()
    return render(request, 'jobs/giver.html', {'job_types': job_types})


@login_required
def seeker(request):
    return render(request, 'jobs/seeker.html')


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
    skills = Skills.objects.filter(job_type_id=2)
    return render(request, 'jobs/post_job.html', {'type': type, 'skills': skills})
