from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import Select
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from dynamic_forms import DynamicField, DynamicFormMixin
from .models import Subscription, CustomUser, Fee
from django.utils.translation import gettext_lazy as _
import datetime
from datetime import date

class CreateEnrollForm(DynamicFormMixin, forms.ModelForm):

        
    def user_charge(ModelForm):
        user = ModelForm['user'].value()
        print('user')
        print(user)
        if user:
            userselec = CustomUser.objects.get(id=user)
            print('userselec')
            print(userselec)
            feecharge = userselec.feecharge
            print('feecharge')
            print(feecharge)
            user = CustomUser.objects.get(id=user)
            feecharge = user.feecharge
            return feecharge
        return None

    def sub_choises(ModelForm):
        user = ModelForm['user'].value()
        print('user')
        print(user)
        # usersub = Fee.objects.select_related('subscription').filter(user=user).values('subscription')
        fees = Fee.objects.filter(user=user)
        subscriptions = Subscription.objects.filter(id__in=fees.values_list('subscription_id', flat=True))
        all_subscriptions = Subscription.objects.all()
        remaining_subscriptions = all_subscriptions.exclude(id__in=subscriptions.values_list('id', flat=True))
        # result = subscriptions.union(remaining_subscriptions)

        # plans = subscriptions.values_list('plan', flat=True).distinct()
        print('fees')
        print(fees)
        print('usersub')
        print(subscriptions)
        print('all_subscriptions')
        print(all_subscriptions)
        print('remaining_subscriptions')
        print(remaining_subscriptions)
        # print('result')
        # print(result)
        
       
        # rest = allsub ^ usersub
        
       
        return remaining_subscriptions

    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        label='Locataire')

    # subscription = forms.ModelChoiceField(queryset=Subscription.objects.all(),
    #                                    widget=forms.Select(attrs={'class': 'form-control'}),
    #                                    label='Subs') , initial=1
    subscription = DynamicField(
                    forms.ModelChoiceField,
                    queryset=sub_choises,
                    label='Abonnement',
                    # initial=initial_sub,
    )

    # date_pay = forms.DateField(label='Date', widget=forms.DateInput(attrs={'class': 'form-control form-control-user'}))
    date = forms.DateField(widget=DatePicker(options={'useCurrent': True,'collapse': False,},attrs={'append': 'fa fa-calendar','icon_toggle': True,}), label='Date', initial=date.today())   
    # amount   = forms.DecimalField(label="Charge", widget=TextInput(attrs={'class': 'form-control form-control-user'}))
    amount   = forms.DecimalField(label="Charge", widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    # amount = DynamicField(
    #                 forms.DecimalField,
    #                 queryset=user_charge,
    #                 # initial=initial_sub,
    # )

    # amount = DynamicField(
    #     forms.DecimalField,
    #     label=_("Amount"),
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
    #     initial=user_charge
    # )

    # list_all_sub = forms.ModelChoiceField(label='list_all_sub',widget=forms.Select(attrs={'class': 'form-control'}),)
    

    class Meta:
        model = Fee
        fields = ['user', 'subscription', 'date', 'amount']


class CreatePlanSubForm(forms.ModelForm):
    YEAR_CHOICES = [(r, r) for r in range(2020, datetime.datetime.now().year + 1)]
    year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), label='Année')
    plan = forms.ChoiceField(label='Plan', choices=Subscription.PLAN_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Subscription
        fields = ['year', 'plan']

    def clean(self):
        cleaned_data = super().clean()
        year = cleaned_data.get('year')
        plan = cleaned_data.get('plan')
        if Subscription.objects.filter(year=year, plan=plan).exists():
            raise ValidationError("Un abonnement avec ce plan existe déjà pour cette année.")
        return cleaned_data
