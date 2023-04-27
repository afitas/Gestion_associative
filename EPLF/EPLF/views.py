from django.shortcuts import render
from accounts.models import CustomUser
from managefee.models import Fee, Subscription


def index(request):
    allusers  = CustomUser.objects.all().count()
    listusers = CustomUser.objects.exclude(is_superuser=True)
    listfee  = Fee.objects.prefetch_related('subscription').all()
    listsub = Subscription.objects.all
    # print(listfee[0].__dict__)
    return render(request, 'index.html', {
        'allusers': allusers,
        'listusers': listusers,
        'listfee': listfee,
        'listsub': listsub,

    }
)