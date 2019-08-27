from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from .forms import *
from .models import *
from jobs.match import count
from jobs.khalti import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import requests
from django.http import JsonResponse
from django.core import serializers


def index(request):
    profile = Profile.objects.all()
    job_types = JobType.objects.all()

    context = {'profile': profile, 'job_types': job_types}
    return render(request, 'jobs/index.html', context)


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
            messages.success(request, 'Job Added')

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
            messages.success(request, 'Job Posted')

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
            messages.success(request, 'Job Applied')

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
            messages.success(request, 'Facility added')
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

        messages.success(request, 'Skill Added Successfully')
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
    # match = Match()

    p = c[0]
    a = c[1]
    s = c[2]
    posted = []
    applied = []
    matches = []
    test = []
    test_p = []
    test_a = []
    m = Match.objects.all()
    for n in m:
        test.append((n.posted_id, n.applied_id, n.score))
        test_p.append((n.posted_id))
        test_a.append((n.applied_id))
    # print(test)
    # print(test_p)
    # print(test_a)
    # print(p)
    # print(a)
    # print(s)
    for i, j, l in zip(p, a, s):
        if (i, j, l) not in test:
            for post in PostedJob.objects.filter(id=i):
                posted.append(post.user.email)
                email_posted([post.user.email])
            for apply in AppliedJob.objects.filter(id=j):
                applied.append(apply.user.email)
                email_applied([apply.user.email])

    print(posted)
    print(applied)

    for k in range(len(p)):
        matches.append((p[k], a[k], s[k]))
        if (p[k], a[k], s[k]) not in test:
            match = Match()
            match.posted_id = p[k]
            match.applied_id = a[k]
            match.score = s[k]
            match.save()

    print(matches)

    return render(request, 'jobs/match.html', {'match': matches})


def email_posted(recipient):
    subject = 'Match Found'
    message_posted = ' We have found the best match for the job you had posted. Please Check you account to find the detail and for payment '
    send_mail(subject, message_posted,
              'DJ Group <settings.EMAIL_HOST_USER>', recipient)


def email_applied(recipient):
    subject = 'Match Found'
    message_applied = ' We have found the best match for the job you needed. Please Check you account to find the detail and for payment '
    send_mail(subject, message_applied,
              'DJ Group <settings.EMAIL_HOST_USER>', recipient)
    return redirect('/')


@login_required
def payment(request, id):
    person = get_object_or_404(User, id=id)
    jobtypes = JobType.objects.all()
    if request.method == 'POST':
        form = PaymentForm(request.POST or None)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.save()
            return redirect('jobs:index')
    else:
        form = PaymentForm()
    context = {
        'jobtypes': jobtypes,
        'form': form,
        'person': person
    }

    return render(request, 'jobs/payment.html', context)


def esewa(request, id):
    person = get_object_or_404(User, id=id)
    url1 = "https://khalti.com/api/v2/payment/verify/"
    # token = "akpSfqg2wKwcN8dBo7ZbwY"
    # v = verification(url1, token, 20000)
    url2 = "https://khalti.com/api/v2/merchant-transaction/"
    t = transaction_list(url2)

    # print(v)
    for i in t['records']:
        print(i['amount'])
        print(i['user']['name'])
        print(i['user']['mobile'] + "\n")
    # print(t[''])

    return render(request, 'jobs/esewa.html', {'t': t, 'person': person})

