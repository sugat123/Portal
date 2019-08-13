from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import *
from .models import *
from jobs.match import count
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    profile = Profile.objects.all()
    job_types = JobType.objects.all()
    return render(request, 'jobs/index.html', {'profile': profile, 'job_types': job_types})


@login_required
def dashboard(request):
    job_types = JobType.objects.all()
    context = {'job_types': job_types}
    return render(request, 'jobs/dashboard.html', context)


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

    facilities = Facility.objects.all()
    # selected_skill = Skills.objects.filter(
    #     id__in=request.POST.getlist('skill'))
    # print(selected_skill)
    # selected_facility = Facility.objects.filter(
    #     id__in=request.POST.getlist('facility'))
    # print(selected_facility)
    if request.method == 'POST':

        form = AddPostedJobForm(request.POST or None)

        if form.is_valid():

            form.save()

            return redirect('jobs:dashboard')
    else:
        form = AddPostedJobForm()

    context = {'type': type,
               'skills': skills,

               'facilities': facilities,
               'form': form}

    return render(request, 'jobs/apply_job.html', context)


@login_required
def apply_job(request, slug):
    type = get_object_or_404(JobType, slug=slug)
    skills = Skills.objects.all()
    facilities = Facility.objects.all()
    if request.method == 'POST':
        form = AddAppliedJobForm(request.POST or none)
        if form.is_valid():
            form.save()
            return redirect('jobs:dashboard')
    else:
        form = AddAppliedJobForm()
    context = {'type': type,
               'skills': skills,
               'facilities': facilities,
               'form': form}
    return render(request, 'jobs/apply_job.html', context)


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

            return redirect(request.META['HTTP_REFERER'])
    else:
        form = AddFacilityForm()
    return render(request, 'jobs/add_facility.html', {'form': form})


@login_required
def add_skill(request):

    if request.method == 'POST':
        form = AddSkillForm(request.POST or None)
        if form.is_valid():
            form.save()

            # return redirect(request.META['HTTP_REFERER'])
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = AddSkillForm()

    return render(request, 'jobs/add_skill.html', {'form': form})


@login_required
def job_list(request, slug):
    type = get_object_or_404(JobType, slug=slug)

    posted_jobs = PostedJob.objects.all().order_by('-created')
    applied_jobs = AppliedJob.objects.all().order_by('-created')

    context = {'posted_jobs': posted_jobs,
               'applied_jobs': applied_jobs,
               'type': type}

    return render(request, 'jobs/job_list.html', context)

# @login_required
# def job_list_giver(request, slug):
#     type = get_object_or_404(JobType, slug=slug)


#     applied_jobs = AppliedJob.objects.all().order_by('created')

#     context = {
#                'applied_jobs': applied_jobs,
#                'type': type}

#     return render(request, 'jobs/job_list.html', context)


@login_required
def posted_job_detail(request, slug, id):
    type = get_object_or_404(JobType, slug=slug)
    posted_jobs = get_object_or_404(
        PostedJob.objects.order_by('-created'), id=id)
    # applied_jobs = AppliedJob.objects.get(id=id)

    context = {'posted_jobs': posted_jobs,
               #   'applied_jobs': applied_jobs,
               'type': type}

    return render(request, 'jobs/posted_job_detail.html', context)


@login_required
def applied_job_detail(request, slug, id):
    type = get_object_or_404(JobType, slug=slug)
    # posted_jobs = PostedJob.objects.get(id=id)
    applied_jobs = get_object_or_404(
        AppliedJob.objects.order_by('-created'), id=id)

    context = {  # 'posted_jobs': posted_jobs,
        'applied_jobs': applied_jobs,
        'type': type}

    return render(request, 'jobs/applied_job_detail.html', context)


def match(request):

    c = count()

    p = c[0]
    a = c[1]
    posted = []
    applied = []
    matches = []
    for k in range(len(p)):
        matches.append((p[k], a[k]))

    print(matches)

    for i in p:
        for post in PostedJob.objects.filter(id=i):
            posted.append(post.user.email)
    print(posted)

    for j in a:
        for apply in AppliedJob.objects.filter(id=j):
            applied.append(apply.user.email)
    print(applied)

    subject_posted = 'Match Found'
    message_posted = ' We have found the best match for the job you had posted. Please Check you account to find the detail and for payment '
    # email_from = settings.EMAIL_HOST_USER
    recipient_list_posted = [posted]

    send_mail(subject_posted, message_posted,
              'DJ Group <settings.EMAIL_HOST_USER>', recipient_list_posted)

    subject_applied = 'Match Found'
    message_applied = ' We have found the best match for the job you needed. Please Check you account to find the detail and for payment '
    # email_from = settings.EMAIL_HOST_USER
    recipient_list_applied = [applied]

    send_mail(subject_applied, message_applied,
              'DJ Group <settings.EMAIL_HOST_USER>', recipient_list_applied)

    return render(request, 'jobs/match.html', {'match': matches})


def email(request):
    subject = 'Match Found'
    message = ' We have found the best match for the job you had posted. Please Check you account to find the detail and for payment '
    # email_from = settings.EMAIL_HOST_USER
    recipient_list = ['sugatp454@gmail.com', 'kshitishpokharel@gmail.com', ]

    send_mail(subject, message,
              'DJ Group <settings.EMAIL_HOST_USER>', recipient_list)

    return redirect('/')
