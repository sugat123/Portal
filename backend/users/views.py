from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from jobs import urls
from .models import ActivationCode
from django.core.mail import send_mail
from .forms import *
from django.http import Http404
from jobs.views import dashboard
from django.views.decorators.cache import never_cache


@never_cache
def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('jobs:dashboard'))
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                # redirect_url = request.GET.get('next', 'users/base')
                # messages.info(request, 'You are logged in as an admin .')

                messages.success(
                    request, '{} Logged in successfully'.format(user.username))
                return redirect('jobs:dashboard')

            # elif user and user.is_staff:
            #     login(request, user)
            #     if not remember_me:
            #         request.session.set_expiry(0)
            #     redirect_url = request.GET.get('next', 'admin:dashboard')
            #     messages.info(request, 'You are logged in as a staff member.')
            #     return redirect(redirect_url)
            elif user and not user.is_active:
                messages.info(request, 'Your account is not active now.')
            else:

                messages.error(request, 'Invalid Username or Password')

        else:

            messages.error(request, 'Invalid Form')

    else:

        form = LoginForm()
    

    return render(request, 'users/login.html', {'form': form})


def logout_user(request):

    if request.user.is_authenticated:
        logout(request)

        return redirect('/')


@never_cache
def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('jobs:dashboard'))
    if request.method == "POST":
        user_form = AddUserForm(request.POST or None)
        profile_form = ProfileForm(request.POST or None)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            code = ActivationCode.objects.create(user=user)
            send_mail(
                'Activate Your Account',
                'Here is the activation code: %s' % code.code,
                'from@example.com',
                [user.email]
            )

            return render(request, 'users/activation_sent.html')

    else:
        user_form = AddUserForm()
        profile_form = ProfileForm()
    return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})

@never_cache
def check_activation_code(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('jobs:dashboard'))
    for i in ActivationCode.objects.all():
        if request.method == 'POST':
            if i.code == request.POST['activation_code']:
                i.user.is_active = True
                i.user.save()
                i.delete()

                messages.success(
                    request, 'Your account has been successfully activated. Please login to continue')
                return redirect('users:login_user')
            else:
                messages.error(request, "Please enter a valid code.")
    return render(request, 'users/activation_sent.html', {})
