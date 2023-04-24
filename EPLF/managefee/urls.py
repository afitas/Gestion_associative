from django.contrib.auth.decorators import login_required
from django.urls import path
from .models import Subscription, CustomUser, Fee
from . import views

urlpatterns = [
    # path('', login_required(views.index), name='enroll.index'),
    path('subscriptions_list/', login_required(views.subscriptions_list), name='enroll.subscriptions_list'),
    path('subscriptions_list/create/', login_required(views.create), name="enroll.create"),
    path('subscription/plan_list/', login_required(views.plan_list), name='subscription.plan_list'),
    path('subscription/plan_create/', login_required(views.plan_create), name="subscription.plan_create"),
    path('subscription/store/', login_required(views.plan_store), name="subscription.store"),
    path('get_course_total_amount/', login_required(views.get_course_total_amount),
         name="enroll.get_course_total_amount"),
    path('subscriptions_list/store/', login_required(views.store), name="enroll.store"),
    path('sub/', login_required(views.sub), name="enroll.sub"),
    path('subscription_amount/<int:user_id>/', login_required(views.subscription_amount), name="enroll.subscription_amount"),
    path('subscriptions_list/edit/<int:eid>', login_required(views.edit), name="enroll.edit"),
    path('subscriptions_list/update/<int:eid>', login_required(views.update), name="enroll.update"),
    path('subscriptions_list/delete/<int:eid>', login_required(views.delete), name="enroll.delete"),
]
