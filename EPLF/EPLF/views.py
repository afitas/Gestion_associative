from django.shortcuts import render
from accounts.models import CustomUser
from managefee.models import Fee


def index(request):
    allusers  = CustomUser.objects.all().count()
    listusers = CustomUser.objects.all().order_by('-username')
    listfee  = Fee.objects.prefetch_related('subscription').all()
    print(listfee[0].__dict__)
    return render(request, 'index.html', {
        'allusers': allusers,
        'listusers': listusers,
        'listfee': listfee,
    }
)