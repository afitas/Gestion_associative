from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from dynamic_forms import DynamicField, DynamicFormMixin
from .models import Subscription, CustomUser, Fee
from django.utils.translation import gettext_lazy as _

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
                                        label='Users')

    # subscription = forms.ModelChoiceField(queryset=Subscription.objects.all(),
    #                                    widget=forms.Select(attrs={'class': 'form-control'}),
    #                                    label='Subs') , initial=1
    subscription = DynamicField(
                    forms.ModelChoiceField,
                    queryset=sub_choises,
                    # initial=initial_sub,
    )

    # date_pay = forms.DateField(label='Date', widget=forms.DateInput(attrs={'class': 'form-control form-control-user'}))
    date = forms.DateField(widget=DatePicker(options={'useCurrent': True,'collapse': False,},attrs={'append': 'fa fa-calendar','icon_toggle': True,}),label='Date')   
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
