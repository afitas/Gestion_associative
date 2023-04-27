from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.forms import LoginForm, EditProfileForm, ChangePasswordForm
from . import models
from . import forms

# from django.shortcuts import render
# # accounts/views.py
# from django.urls import reverse_lazy
# from django.views.generic.edit import CreateView

# from .forms import CustomUserCreationForm

# class SignUpView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if 'remember' not in request.POST:
                request.session.set_expiry(0)

            if 'next' in request.POST:
                return redirect(request.POST['next'])
            else:
                return redirect('index')
        else:
            return render(request, 'account/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    else:
        return redirect('index')


def profile_edit(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account.profile')
        else:
            return render(request, 'account/profile.edit.html', {'form': form})
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'account/profile.edit.html', {'form': form})


def profile_view(request):
    return render(request, 'account/profile.html')


def password_change(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('account.profile')
        else:
            return render(request, 'account/profile.password.html', {'form': form})
    else:
        form = ChangePasswordForm(request.user)
        return render(request, 'account/profile.password.html', {'form': form})

def list(request):
    listusers = models.CustomUser.objects.exclude(is_superuser=True)
    return render(request, 'account/list.html', {'listusers': listusers})

def create(request):
    form = forms.CreateuserForm()
    return render(request, 'account/create.html', {'form': form})

def store(request):
    if request.method == 'POST':
        form = forms.CreateuserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully')
            return redirect('users.list')
        else:
            return render(request, 'account/create.html', {'form': form})
    else:
        return redirect('users.create')
    
def edit(request, uid):
    try:
        user = models.CustomUser.objects.get(id=uid)
        form = forms.CreateuserForm(instance=user)
        return render(request, 'account/edit.html', {'form': form})
    except models.CustomUser.DoesNotExist:
        return redirect('users.list')
    
def update(request, uid):
    if request.method == 'POST':
        try:
            user = models.CustomUser.objects.get(id=uid)
            form = forms.CreateuserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'User updated successfully')
                return redirect('users.list')
            else:
                return render(request, 'account/edit.html', {'form': form})
        except models.CustomUser.DoesNotExist:
            return redirect('users.list')
    else:
        return redirect('users.list')


def delete(request, uid):
    if request.method == 'POST':
        try:
            user = models.CustomUser.objects.get(id=uid)
            user.delete()
            messages.success(request, 'User deleted successfully')
            return redirect('users.list')
        except models.CustomUser.DoesNotExist:
            return redirect('users.list')
    else:
        return redirect('users.list')

