from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *


def index(request):
    return render(request, 'jobs/index.html')


@login_required
def giver(request):
    return render(request, 'jobs/giver.html')


@login_required
def seeker(request):
    return render(request, 'jobs/seeker.html')


@login_required
def add_job(request):
    if request.method == 'POST':
        form = AddJobTypeForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('jobs:index')
    else:
        form = AddJobTypeForm()

    return render(request, 'jobs/add_job.html', {'form': form})
