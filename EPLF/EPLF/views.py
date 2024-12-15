from accounts.models import CustomUser
from django.shortcuts import render, redirect


def index(request):
    # Redirection selon le rôle
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        else:
            return redirect('tenant_dashboard')
    
    return redirect('account.login')