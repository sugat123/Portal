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
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q


from itertools import chain
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    profile = Profile.objects.all()
    job_types = JobType.objects.all()
    
    context = {'profile': profile, 'job_types': job_types}
    return render(request, 'jobs/index.html', context)


@login_required
def dashboard(request):
    job_types = JobType.objects.all()

    c = count()
    # match = Match()

    p = c[0]
    a = c[1]
    s = c[2]
    job = c[3]

    posted = []
    applied = []
    matches = []
    test = []
    test_p = []
    test_a = []

    for n in Match.objects.all():
        test.append((n.posted_id, n.applied_id, n.score))
        test_p.append((n.posted_id))
        test_a.append((n.applied_id))

    for i, j, l in zip(p, a, s):
        if (i, j, l) not in test:
            for post in PostedJob.objects.filter(id=i):
                posted.append(post.user.email)
                text1 = ' We have found the best match for the job you had posted. Please Check you account to find the detail and for payment '
                email_match([post.user.email], text1)
                
                # sms(post.user.profile.number, text1)
            for apply in AppliedJob.objects.filter(id=j):
                applied.append(apply.user.email)
                text2 = ' We have found the best match for the job you needed. Please Check you account to find the detail and for payment '
                email_match([apply.user.email], text2)
                
                # sms(apply.user.profile.number, text2)

    for k in range(len(p)):

        matches.append((p[k], a[k], s[k]))
        if (p[k], a[k], s[k]) not in test:
            match = Match()
            match.posted_id = p[k]
            match.applied_id = a[k]
            match.score = s[k]
            match.job_type = job[k]
            match.save()

    print(matches)
    
    
    page = request.GET.get('page')
    paginator = Paginator(job_types, 3)
    job_types = paginator.get_page(page)
    
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    context = {'job_types': job_types, 'users': users}
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


# def match(request):

#     c = count()
#     # match = Match()

#     p = c[0]
#     a = c[1]
#     s = c[2]
#     job = c[3]

#     posted = []
#     applied = []
#     matches = []
#     test = []
#     test_p = []
#     test_a = []
#     m = Match.objects.all()
#     for n in m:
#         test.append((n.posted_id, n.applied_id, n.score))
#         test_p.append((n.posted_id))
#         test_a.append((n.applied_id))
#     # print(test)
#     # print(test_p)
#     # print(test_a)
#     # print(p)
#     # print(a)
#     # print(s)
#     for i, j, l in zip(p, a, s):
#         if (i, j, l) not in test:
#             for post in PostedJob.objects.filter(id=i):
#                 posted.append(post.user.email)
#                 email_posted([post.user.email])
#             for apply in AppliedJob.objects.filter(id=j):
#                 applied.append(apply.user.email)
#                 email_applied([apply.user.email])

#     # print(posted)
#     # print(applied)

#     for k in range(len(p)):

#         matches.append((p[k], a[k], s[k]))
#         if (p[k], a[k], s[k]) not in test:
#             match = Match()
#             match.posted_id = p[k]
#             match.applied_id = a[k]
#             match.score = s[k]
#             match.job_type = job[k]
#             match.save()

#     print(matches)

#     return render(request, 'jobs/match.html', {'match': matches})


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



@login_required
def payment(request):
    paid = Payment.objects.all()
    match = Match.objects.all()
    user = User.objects.all()
    verify = Verification.objects.all()
    test = []
    for l in verify:
        test.append(l.payment_id)
    print(test)

    for i in match:
        for j in paid:
            if j.id not in test:
                if i.applied_id == j.profile_id and i.job_type == j.product:
                    for k in User.objects.filter(id=i.applied_id):
                        for m in User.objects.filter(id=i.posted_id):

                            
                            
                            text1 = "Your payment has been completed and this is the contact number: " + m.profile.number +  " of employeer: "+ m.username + " for job you applied."
                            # sms(k.profile.number, text1 ) #sms to seeker
                            text2 = "Your payment has been completed and this is the contact number: " + k.profile.number +  " of job seeker: "+ k.username + " for the job you posted."
                            # sms(m.profile.number, text2 ) #sms to giver
                            
                            email([k.email], text1)
                            email([m.email], text2)
                            v = Verification()
                            v.payment_id = j.id
                            v.user_id = j.profile_id
                            v.save()

    context = {
        # 'jobtypes': jobtypes,
    }

    return render(request, 'jobs/payment.html', context)


@csrf_exempt
def esewa(request, id):
    person = get_object_or_404(User, id=id)
    applied = AppliedJob.objects.all()
    posted = PostedJob.objects.all()
    

    if request.method == "POST" and request.is_ajax():

        token = request.POST['token']
        amount = request.POST['amount']
        user_id = request.POST['product_identity']
        product = request.POST['product_name']

        v = verification(token, amount)

        if v['state']['name'] == "Completed":
            print("Completed")
            paid = Payment()
            paid.profile_id = user_id
            paid.name = v['user']['name']
            paid.amount = v['amount']
            paid.mobile = v['user']['mobile']
            paid.created_on = v['created_on']
            paid.product = product
            paid.save()

   

                        # url2 = "https://khalti.com/api/v2/merchant-transaction/"
                        # t = transaction_list(url2)

                        # print(v)
                        # for i in t['records']:
                        #     print(i['amount'])
                        #     print(i['user']['name'])
                        #     print(i['user']['mobile'] + "\n")
                        # print(t[''])

    context = {'person': person, 'applied': applied, 'posted': posted}
    return render(request, 'jobs/esewa.html', context)



# def search(request):  # new
#     query = request.GET.get('q')
#     object_list = JobType.objects.filter(
#         Q(title__icontains=query)
#     )
#     context = {'object_list' : object_list}
#     return render(request, 'jobs/search_results.html',context)

class SearchView(ListView):
    template_name = 'jobs/search_results.html'
    count = 0
    paginate_by = 3
    page = request.GET.get('page')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

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