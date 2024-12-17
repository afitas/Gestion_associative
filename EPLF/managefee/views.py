from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import Subscription, CustomUser, Fee
from managefee.forms import CreateEnrollForm, CreatePlanSubForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
import datetime
from .forms import DashboardFilterForm
# Create your views here.


# def index(request):
#     enrolls = Fee.objects.all()
#     return render(request, 'managefee/index.html', {'enrolls': enrolls})

def subscriptions_list(request):
    # Récupérer tous les paiements avec leurs relations
    enrolls = Fee.objects.select_related('user', 'subscription').all()
    
    # Statistiques globales
    total_amount = enrolls.aggregate(Sum('amount'))['amount__sum'] or 0
    total_payments = enrolls.count()
    avg_payment = total_amount / total_payments if total_payments > 0 else 0
    
    # Tendance des paiements par mois
    payments_by_month = (
        Fee.objects.annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    
    context = {
        'enrolls': enrolls,
        'total_amount': total_amount,
        'total_payments': total_payments,
        'avg_payment': avg_payment,
        'payments_by_month': list(payments_by_month)
    }
    
    return render(request, 'managefee/subscriptions_list.html', context)

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

def my_subscriptions(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # Rediriger le superadmin vers la liste des abonnements
            return redirect('enroll.subscriptions_list')

        else:
            # Logique pour l'abonné
            user_fees = Fee.objects.filter(user=request.user).order_by('-subscription__year', 'subscription__plan')
            fees_by_year = {}
            for fee in user_fees:
                year = fee.subscription.year
                if year not in fees_by_year:
                    fees_by_year[year] = []
                fees_by_year[year].append(fee)
            
            # Récupérer les abonnements non payés
            unpaid_subscriptions = Subscription.objects.exclude(id__in=user_fees.values_list('subscription_id', flat=True))

            context = {
                'fees_by_year': fees_by_year,
                'total_amount': sum(fee.amount for fee in user_fees),
                'unpaid_subscriptions': unpaid_subscriptions,  # Ajout des abonnements non payés
            }
            return render(request, 'managefee/my_subscriptions.html', context)

    return redirect('login')

@login_required
def tenant_dashboard(request):
    if request.user.is_authenticated:
        user_fees = Fee.objects.filter(user=request.user)
        
        # Calculer le montant total
        total_amount = sum(fee.amount for fee in user_fees)

        # Récupérer les abonnements de l'utilisateur
        subscriptions = Subscription.objects.filter(fee__user=request.user).distinct()

        # Récupérer les paiements récents (5 derniers)
        recent_payments = user_fees.order_by('-date')[:5]

        # Préparer les données pour le graphique par mois
        payments_by_month = {}
        for fee in user_fees:
            month_key = fee.date.strftime("%Y-%m")
            if month_key in payments_by_month:
                payments_by_month[month_key] += float(fee.amount)
            else:
                payments_by_month[month_key] = float(fee.amount)

        context = {
            'total_amount': total_amount,
            'subscriptions': subscriptions,
            'recent_payments': recent_payments,
            'monthly_data': payments_by_month,
        }
        return render(request, 'managefee/tenant_dashboard.html', context)

    return redirect('login')

# @login_required
def admin_dashboard(request):
    selected_year = request.GET.get('year', datetime.datetime.now().year)
    
    # Récupérer tous les mois de l'année
    months_data = []
    # Exclure le superadmin du décompte total
    total_expected = CustomUser.objects.filter(is_superuser=False).count()
    
    # Statistiques globales pour l'année sélectionnée
    all_fees = Fee.objects.filter(user__is_superuser=False, subscription__year=selected_year)
    total_amount_all = all_fees.aggregate(Sum('amount'))['amount__sum'] or 0
    total_payments_all = all_fees.count()
    avg_payment = total_amount_all / total_payments_all if total_payments_all > 0 else 0

    # Calculer le total des non-paiements pour chaque mois
    total_unpaid = 0
    
    for month_tuple in Subscription.PLAN_CHOICES:
        month_code, month_name = month_tuple
        
        # Obtenir tous les utilisateurs qui n'ont pas payé ce mois
        paid_users = Fee.objects.filter(
            subscription__plan=month_code,
            subscription__year=selected_year,
            user__is_superuser=False
        ).values_list('user_id', flat=True)
        
        # Calculer le total des mensualités des utilisateurs qui n'ont pas payé
        unpaid_amount = CustomUser.objects.filter(
            is_superuser=False
        ).exclude(
            id__in=paid_users
        ).aggregate(
            total=Sum('feecharge')
        )['total'] or 0
        
        total_unpaid += unpaid_amount
        
        # Total des abonnements pour ce mois
        total_subscriptions = Fee.objects.filter(
            subscription__plan=month_code,
            subscription__year=selected_year,
            user__is_superuser=False
        ).count()
        
        # Total des paiements reçus
        total_paid = Fee.objects.filter(
            subscription__plan=month_code,
            subscription__year=selected_year,
            user__is_superuser=False
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Nombre d'abonnés payés
        paid_subscribers = Fee.objects.filter(
            subscription__plan=month_code,
            subscription__year=selected_year,
            user__is_superuser=False
        ).values('user').distinct().count()
        
        # Calcul des pourcentages
        payment_percentage = (paid_subscribers / total_expected * 100) if total_expected > 0 else 0

        months_data.append({
            'code': month_code,
            'name': month_name,
            'total_subscriptions': total_subscriptions,
            'paid_subscribers': paid_subscribers,
            'unpaid_subscribers': total_expected - paid_subscribers,
            'total_paid': total_paid,
            'payment_percentage': round(payment_percentage, 2)
        })
    
    # Années disponibles pour le filtre
    available_years = Fee.objects.dates('date', 'year').values_list('date__year', flat=True).distinct()
    if not available_years:
        available_years = [timezone.now().year]
    
    context = {
        'months_data': months_data,
        'selected_year': int(selected_year),
        'available_years': available_years,
        'total_amount_all': total_amount_all,
        'total_payments_all': total_payments_all,
        'avg_payment': avg_payment,
        'total_unpaid': total_unpaid
    }
    
    return render(request, 'managefee/admin_dashboard.html', context)

def month_details(request, month, year):
    # Récupérer tous les utilisateurs non-superadmin
    all_users = CustomUser.objects.filter(is_superuser=False)
    
    # Récupérer les utilisateurs qui ont payé
    paid_users = Fee.objects.filter(
        subscription__plan=month,
        subscription__year=year,
        user__is_superuser=False
    ).select_related('user', 'subscription').order_by('date')
    
    # Liste des utilisateurs ayant payé
    paid_users_list = []
    for payment in paid_users:
        paid_users_list.append({
            'user': payment.user.username,
            'date': payment.date.strftime('%d/%m/%Y'),
            'amount': str(payment.amount)
        })
    
    # Liste des utilisateurs n'ayant pas payé
    paid_user_ids = paid_users.values_list('user_id', flat=True)
    unpaid_users = all_users.exclude(id__in=paid_user_ids)
    unpaid_users_list = [{'user': user.username} for user in unpaid_users]
    
    return JsonResponse({
        'paid_users': paid_users_list,
        'unpaid_users': unpaid_users_list,
        'total_paid': len(paid_users_list),
        'total_unpaid': len(unpaid_users_list)
    })

@login_required
def filtered_details(request):
    # Récupérer les paramètres de filtrage
    selected_year = request.GET.get('year', datetime.datetime.now().year)
    selected_month = request.GET.get('month', '')
    selected_bloc = request.GET.get('bloc', '')
    
    # Récupérer tous les utilisateurs non-superadmin
    users_query = CustomUser.objects.filter(is_superuser=False)
    
    # Appliquer le filtre de bloc si sélectionné
    if selected_bloc:
        users_query = users_query.filter(bloc=selected_bloc)
    
    # Obtenir tous les utilisateurs concernés
    all_users = users_query.all()
    total_expected = users_query.count()
    
    # Préparer la requête de base pour les paiements
    fees_query = Fee.objects.filter(
        subscription__year=selected_year,
        user__is_superuser=False
    )
    
    # Appliquer le filtre de mois si sélectionné
    if selected_month:
        fees_query = fees_query.filter(subscription__plan=selected_month)
    
    # Appliquer le filtre de bloc
    if selected_bloc:
        fees_query = fees_query.filter(user__bloc=selected_bloc)
    
    # Récupérer les paiements
    paid_users = fees_query.select_related('user', 'subscription').order_by('date')
    
    # Calculer les statistiques
    total_paid = paid_users.aggregate(total=Sum('amount'))['total'] or 0
    paid_count = paid_users.values('user').distinct().count()
    
    # Calculer le total des mensualités impayées
    paid_user_ids = paid_users.values_list('user_id', flat=True).distinct()
    unpaid_users = users_query.exclude(id__in=paid_user_ids)
    total_unpaid = unpaid_users.aggregate(total=Sum('feecharge'))['total'] or 0
    
    # Préparer les données pour le template
    context = {
        'selected_year': int(selected_year),
        'selected_month': selected_month,
        'selected_bloc': selected_bloc,
        'available_years': Fee.objects.dates('date', 'year').values_list('date__year', flat=True).distinct(),
        'available_blocs': CustomUser.BLOC_CHOICES,
        'months': Subscription.PLAN_CHOICES,
        'total_paid': total_paid,
        'total_unpaid': total_unpaid,
        'paid_users': paid_users,
        'unpaid_users': unpaid_users,
        'paid_count': paid_count,
        'unpaid_count': total_expected - paid_count,
        'payment_percentage': (paid_count / total_expected * 100) if total_expected > 0 else 0
    }
    
    return render(request, 'managefee/filtered_details.html', context)


@login_required
def admin_dashboard_stats(request):
    # Vérifier si l'utilisateur est un administrateur
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas l'autorisation d'accéder à cette page.")
        return redirect('tenant_dashboard')
    
    form = DashboardFilterForm(request.GET or None)
    context = {
        'form': form,
        'show_results': False
    }
    
    if request.GET and form.is_valid():
        # Récupérer les données du formulaire
        selected_year = form.cleaned_data['year']
        selected_month = form.cleaned_data['month']
        selected_bloc = form.cleaned_data['bloc']
        
        # Requête de base pour tous les utilisateurs non superadmin
        users_query = CustomUser.objects.filter(is_superuser=False)
        
        # Appliquer les filtres de bloc si sélectionné
        if selected_bloc:
            users_query = users_query.filter(bloc=selected_bloc)
        
        # Total attendu d'abonnés
        total_expected = users_query.count()
        
        # Préparer la requête de base pour les paiements
        fees_query = Fee.objects.filter(
            subscription__year=selected_year,
            user__is_superuser=False
        )
        
        # Appliquer le filtre de mois si sélectionné
        if selected_month:
            fees_query = fees_query.filter(subscription__plan=selected_month)
        
        # Appliquer le filtre de bloc
        if selected_bloc:
            fees_query = fees_query.filter(user__bloc=selected_bloc)
        
        # Obtenir les utilisateurs ayant payé
        paid_users = fees_query.values('user').distinct().count()
        
        # Calculer les statistiques
        total_paid = fees_query.aggregate(total=Sum('amount'))['total'] or 0
        total_expected_amount = users_query.aggregate(total=Sum('feecharge'))['total'] or 0
        
        # Calculer le pourcentage de paiement
        payment_percentage = (paid_users / total_expected * 100) if total_expected > 0 else 0
        
        # Préparer les résultats
        context.update({
            'show_results': True,
            'total_paid_users': paid_users,
            'total_unpaid_users': total_expected - paid_users,
            'payment_percentage': round(payment_percentage, 2),
            'total_paid_amount': total_paid,
            'total_expected_amount': total_expected_amount,
            'selected_year': selected_year,
            'selected_month': selected_month or 'Tous',
            'selected_bloc': selected_bloc or 'Tous'
        })
    
    return render(request, 'managefee/admin_dashboard_stats.html', context)