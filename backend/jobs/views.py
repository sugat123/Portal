from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'jobs/index.html')


@login_required
def giver(request):
    return render(request, 'jobs/giver.html')


@login_required
def seeker(request):
    return render(request, 'jobs/seeker.html')
