# accounts/urls.py
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    # path("signup/", SignUpView.as_view(), name="signup"),
    path('', views.login_view, name='account.login'),
    path('profile/edit/', login_required(views.profile_edit), name='account.profile.edit'),
    path('profile/', login_required(views.profile_view), name='account.profile'),
    path('logout/', login_required(views.logout_view), name='account.logout'),
    path('profile/password/', login_required(views.password_change), name='account.password.change'),

    path('users/list/', login_required(views.list), name='users.list'),
    path('users/create/', login_required(views.create), name="users.create"),
    path('store/', login_required(views.store), name="users.store"),
    path('edit/<int:uid>/', login_required(views.edit), name="users.edit"),
    path('update/<int:uid>/', login_required(views.update), name="users.update"),
    path('delete/<int:uid>/', login_required(views.delete), name="users.delete"),
]   