from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import Select
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from .models import Subscription, CustomUser, Fee
import datetime
from datetime import date

class CreateEnrollForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.exclude(is_superuser=True), widget=forms.Select(attrs={'class': 'form-control'}), label='Locataire')
    subscription = forms.ModelChoiceField(queryset=Subscription.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}), label='Abonnement')
    date = forms.DateField(widget=DatePicker(options={'useCurrent': True,'collapse': False,},attrs={'append': 'fa fa-calendar','icon_toggle': True,}), label='Date')
    amount = forms.DecimalField(label="Charge", widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    class Meta:
        model = Fee
        fields = ['user', 'subscription', 'date', 'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subscription'].queryset = Subscription.objects.none()

        # Initialiser la date avec la date actuelle
        self.fields['date'].initial = date.today()

        if 'user' in self.data:
            self.fields['subscription'].queryset = self.get_remaining_subscriptions(self['user'].value())

    def get_remaining_subscriptions(self, user_id):
        user = CustomUser.objects.get(pk=user_id)
        enrolled_subscriptions = Fee.objects.filter(user=user).values_list('subscription', flat=True)
        return Subscription.objects.exclude(pk__in=enrolled_subscriptions)


class CreatePlanSubForm(forms.ModelForm):
    plan = forms.ChoiceField(label='Plan', choices=Subscription.PLAN_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Subscription
        fields = ['year', 'plan']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamiquement définir les options pour l'année lors de la création du formulaire
        self.fields['year'] = forms.ChoiceField(
            choices=self.get_year_choices(),
            initial=datetime.datetime.now().year,  # Définir l'année actuelle comme valeur par défaut
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Année'
        )

    def get_year_choices(self):
        # Définir dynamiquement les options pour l'année en fonction de l'année actuelle
        return [(r, r) for r in range(2020, datetime.datetime.now().year + 1)]

    def clean(self):
        cleaned_data = super().clean()
        year = cleaned_data.get('year')
        plan = cleaned_data.get('plan')
        if Subscription.objects.filter(year=year, plan=plan).exists():
            raise ValidationError("Un abonnement avec ce plan existe déjà pour cette année.")
        return cleaned_data