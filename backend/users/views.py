from django.urls import reverse_lazy
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from jobs import urls

from .forms import *


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(request, username=username, password=password)
            if user and user.is_superuser:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                # redirect_url = request.GET.get('next', 'users/base')
                # messages.info(request, 'You are logged in as an admin .')
                return redirect('jobs:index')
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
                messages.error(request, 'Invalid Username and Password')
        else:
            messages.error(request, 'Invalid Form')

    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_user(request):

    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'logged out successfully')
        return redirect('users:login_user')


def register(request):
    if request.method == "POST":
        form = AddUserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(
                request, 'user created with username {}'.format(user.username))
            return redirect('register')
    else:
        form = AddUserForm()
    return render(request, 'users/register.html', {'form': form})
