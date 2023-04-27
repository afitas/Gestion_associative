from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import Select
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from .models import Subscription, CustomUser, Fee
import datetime
from datetime import date

class CreateEnrollForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), label='Locataire')
    subscription = forms.ModelChoiceField(queryset=Subscription.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}), label='Abonnement')
    date = forms.DateField(widget=DatePicker(options={'useCurrent': True,'collapse': False,},attrs={'append': 'fa fa-calendar','icon_toggle': True,}), label='Date', initial=date.today())   
    amount = forms.DecimalField(label="Charge", widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    class Meta:
        model = Fee
        fields = ['user', 'subscription', 'date', 'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subscription'].queryset = Subscription.objects.none()

        if 'user' in self.data:
            self.fields['subscription'].queryset = self.get_remaining_subscriptions(self['user'].value())

    def get_remaining_subscriptions(self, user_id):
        user_subscriptions = Subscription.objects.filter(fee__user=user_id)
        remaining_subscriptions = Subscription.objects.exclude(id__in=user_subscriptions)
        return remaining_subscriptions



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
