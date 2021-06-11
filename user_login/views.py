from django.shortcuts import render, HttpResponseRedirect
from .models import User, Profile
from .forms import ProfileForm, SingUpCreateUserForm

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
# messages
from django.contrib import messages


# Create your views here.

def Sing_up(request):
    form = SingUpCreateUserForm()
    if request.method == 'POST':
        form = SingUpCreateUserForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully .')
            return HttpResponseRedirect(reverse('user_login:login'))

    data = {
        "title": "sing_up page",
        "form": form,
    }
    return render(request, 'user_login/sing_up.html', data)


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_shop:homepage'))
    data = {
        "title": 'login page',
        "form": form,
    }
    return render(request, 'user_login/login.html', data)


@login_required
def Log_out(request):
    logout(request)
    messages.warning(request, 'Your are logged Out')
    return HttpResponseRedirect(reverse('App_shop:homepage'))


@login_required
def user_profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        form.save()
        messages.success(request, 'Profile details updated.')
        form = ProfileForm(instance=profile)
    data = {
        "title": 'Edit_profile',
        "form": form,
    }

    return render(request, 'user_login/Edit_profile.html', data)
