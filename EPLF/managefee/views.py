from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import Subscription, CustomUser, Fee
from managefee.forms import CreateEnrollForm, CreatePlanSubForm

# Create your views here.


# def index(request):
#     enrolls = Fee.objects.all()
#     return render(request, 'managefee/index.html', {'enrolls': enrolls})

def subscriptions_list(request):
    enrolls = Fee.objects.all()
    return render(request, 'managefee/subscriptions_list.html', {'enrolls': enrolls})

def plan_list(request):
    allSubscription = Subscription.objects.all()
    return render(request, 'managefee/plan_list.html', {'allSubscription': allSubscription})


def create(request):
    form = CreateEnrollForm()
    return render(request, 'managefee/create.html', {'form': form})

def plan_create(request):
    form = CreatePlanSubForm()
    return render(request, 'managefee/plan_create.html', {'form': form})

def plan_store(request):
    if request.method == 'POST':
        form = CreatePlanSubForm(request.POST or None)
        
        if form.is_valid():
            # print("tesssssssssst")
            # print(form)
            form.save()
            messages.success(request, 'Ce plan à bien étais enregistrer')
            return redirect('subscription.plan_list')
        else:
            return render(request, 'managefee/plan_create.html', {'form': form})
    else:
        return redirect('subscription.plan_list')



def get_course_total_amount(request):
    # print("request")
    # print(request.__dict__)
    user = CustomUser.objects.get(id=request.POST.get('course_id'))
    # print("user.feecharge")
    # print(user.feecharge)
    return JsonResponse({'data': user.feecharge})

def subscription_amount(request, user_id):
    print('request_id_js')
    print(request)
    # print(user_id)
    # user_id = request.GET.get('user_id')
    # print('user_id_js')
    print(user_id)
    if user_id:
        user = CustomUser.objects.get(id=user_id)
        feecharge = user.feecharge
        return JsonResponse({'feecharge': feecharge})
    else:
        return JsonResponse({'error': 'User ID not provided'})

def sub(request):
    form = CreateEnrollForm(request.GET)
    print(form['subscription'])
    return HttpResponse(form['subscription'])    


def store(request):
    # user = Fee.objects.get(id=request.POST.get('user'))
    # print("user")
    # print(user)
    if request.method == 'POST':
        form = CreateEnrollForm(request.POST or None)
        print("request.POST")
        print(request.POST)
        if form.is_valid():
            # print("tesssssssssst")
            # print(form)
            form.save()
            messages.success(request, 'Charge for user successfully store')
            return redirect('enroll.subscriptions_list')
        else:
            return render(request, 'managefee/create.html', {'form': form})
    else:
        return redirect('enroll.subscriptions_list')


def edit(request, eid):
    try:
        enroll = Fee.objects.get(id=eid)
        form = CreateEnrollForm(instance=enroll)
        return render(request, 'managefee/edit.html', {'form': form, 'enroll': enroll})
    except Fee.DoesNotExist:
        return redirect('enroll.subscriptions_list')


def update(request, eid):
    try:
        if request.method == 'POST':
            enroll = Fee.objects.get(id=eid)
            form = CreateEnrollForm(request.POST, instance=enroll)
            if form.is_valid():
                form.save()
                messages.success(request, 'info for user successfully updated ')
                return redirect('enroll.subscriptions_list')
            else:
                return render(request, 'managefee/edit.html', {'form': form, 'enroll': enroll})
        else:
            return redirect('enroll.subscriptions_list')
    except Fee.DoesNotExist:
        return redirect('enroll.subscriptions_list')


def delete(request, eid):
    if request.method == 'POST':
        try:
            enroll = Fee.objects.get(id=eid)
            enroll.delete()
            return redirect('enroll.subscriptions_list')
        except Fee.DoesNotExist:
            messages.error(request, 'Enrolled info not found')
            return redirect('enroll.subscriptions_list')
    else:
        messages.error(request, 'Invalid request')
        return redirect('enroll.subscriptions_list')

