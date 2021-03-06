from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from .forms import *
from .models import *
from jobs.match import count, match
from jobs.exchange import exchange, verify
from jobs.khalti import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import requests
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
import re
import datetime
from django.db.models import Q
from itertools import chain
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    profile = Profile.objects.all()
    job_types = JobType.objects.all()
    # path = request.get_full_path()[2:]
    
    # if 'oid' in path:
    #     data = re.split('oid=+|&amt=+|\&refId=', path)
    #     del data[0]
    #     url ="https://uat.esewa.com.np/epay/transrec"
    #     d = {
    #         'amt': data[1],
    #         'scd': 'NP-ES-EPAY',
    #         'rid': data[2],
    #         'pid': data[0],
    #     }
    #     resp = requests.post(url, d)
    #     print(resp.text)
    #     test = []
    #     for i in Payment.objects.all():
    #         test.append((i.profile_id, i.name, i.amount,  i.mobile))
    #     if (request.user.id, request.user.username, data[1], request.user.profile.number) not in test:
    #         paid = Payment()
    #         paid.profile_id = request.user.id
    #         paid.name = request.user.username
    #         paid.amount = data[1]
    #         for temp in JobType.objects.filter(id = data[0]):
    #             paid.product = temp.title
    #         paid.mobile = request.user.profile.number
    #         paid.created_on = datetime.datetime.now()
    #         paid.save()
    

    context = {'profile': profile, 'job_types': job_types}
    return render(request, 'jobs/index.html', context)


def main(request):
    return render(request, 'jobs/main.html')

def dashboard(request):
    job_types = JobType.objects.all()
    path = request.get_full_path()[2:]
    
    if 'oid' in path:
        data = re.split('oid=+|&amt=+|\&refId=', path)
        del data[0]
        url ="https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': data[1],
            'scd': 'NP-ES-EPAY',
            'rid': data[2],
            'pid': data[0],
        }
        resp = requests.post(url, d)
        print(resp.text)
        test = []
        for i in Payment.objects.all():
            test.append((i.profile_id, i.name, i.amount,  i.mobile))
        if (request.user.id, request.user.username, data[1], request.user.profile.number) not in test:
            paid = Payment()
            paid.profile_id = request.user.id
            paid.name = request.user.username
            paid.amount = data[1]
            
            pid = data[0]
            p = int(pid[0])
           
            for temp in JobType.objects.filter(id = p):
                paid.product = temp.id
            paid.mobile = request.user.profile.number
            paid.created_on = datetime.datetime.now()
            paid.save()

    c = count()
    match(c)

    verify()
    exchange()

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
        form = AddAppliedJobForm(request.POST or None)
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
            facility = form.save(commit=False)
            facility.save()
            # messages.success(request, 'Facility added')
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

        # messages.success(request, 'Skill Added Successfully')
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


def email_match(recipient, text):
    subject = 'Match Found'
    send_mail(subject, text,
              'DJ Group <settings.EMAIL_HOST_USER>', recipient)


def email(recipient, text):
    subject = 'Contact Detail'
    
    send_mail(subject, text,
              'DJ Group <settings.EMAIL_HOST_USER>', recipient)
    return redirect('/')


def sms(number, text):
    r = requests.post(
            "http://api.sparrowsms.com/v2/sms/",
            data={'token' : 'I53mEFe0oi8oOC0BrMLv',
                  'from'  : 'Demo',
                  'to'    : number,
                  'text'  : text})
    

    status_code = r.status_code
    # response = r.text
    response_json = r.json()
    print(status_code)
    # print(response)
    print(response_json)
    return r


@csrf_exempt
def khalti(request, id):
    person = User.objects.all()
    match = get_object_or_404(Match, id=id)

    applied = AppliedJob.objects.all()
    posted = PostedJob.objects.all()
    

    if request.method == "POST" and request.is_ajax():

        token = request.POST['token']
        amount = request.POST['amount']
        # user_id = request.POST['product_identity']
        product = request.POST['product_identity']

        v = verification(token, amount)

        if v['state']['name'] == "Completed":
            print("Completed")
            paid = Payment()
            paid.profile_id = request.user.id
            paid.name = v['user']['name']
            paid.amount = int(v['amount']) / 100
            paid.mobile = v['user']['mobile']
            paid.created_on = v['created_on']
            paid.product = int(product)
            paid.save()

   

                        # url2 = "https://khalti.com/api/v2/merchant-transaction/"
                        # t = transaction_list(url2)

                        # print(v)
                        # for i in t['records']:
                        #     print(i['amount'])
                        #     print(i['user']['name'])
                        #     print(i['user']['mobile'] + "\n")
                        # print(t[''])

    context = {'person': person, 'applied': applied, 'posted': posted, 'match':match}
    return render(request, 'jobs/khalti.html', context)


class SearchView(ListView):
    model = JobType
    template_name = 'jobs/search_results.html'
    count = 0
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None).replace(" ", "")

        if query is not None:
            job_results = JobType.objects.search(query)
            

            # # combine querysets
            # queryset_chain = chain(
            #     job_results,
                
            # )
            qs = sorted(job_results,
                        key=lambda instance: instance.pk,
                        reverse=True)
            print (qs)
            self.count = len(qs)  # since qs is actually a list
            return qs
        return JobType.objects.none()

    # def get_queryset(self):  # new
    #     query = self.request.GET.get('q')
    #     object_list = JobType.objects.filter(
    #         Q(title__icontains=query) | Q(slug__icontains=query)
    #     )
    #     return object_list


def error_404_view(request, exception):
    return render(request, 'jobs/error_404.html',{})