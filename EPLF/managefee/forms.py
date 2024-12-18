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

class DashboardFilterForm(forms.Form):
    YEAR_CHOICES = [(r, r) for r in range(1980, datetime.datetime.now().year + 1)]
    
    year = forms.ChoiceField(
        choices=YEAR_CHOICES, 
        initial=datetime.datetime.now().year,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    month = forms.ChoiceField(
        choices=[('', 'Tous les mois')] + list(Subscription.PLAN_CHOICES),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    bloc = forms.ChoiceField(
        choices=[('', 'Tous les blocs')] + list(CustomUser.BLOC_CHOICES),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    export = forms.BooleanField(
        label='Exporter en CSV',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class AdminDashboardGlobalForm(forms.Form):
    YEAR_CHOICES = [(r, r) for r in range(1980, datetime.datetime.now().year + 1)]
    
    year = forms.ChoiceField(
        choices=YEAR_CHOICES, 
        initial=datetime.datetime.now().year,
        label='Année',
        widget=forms.Select(attrs={
            'class': 'form-control custom-select custom-select-sm',
            'style': 'max-width: 200px;'
        })
    )

class AdminDashboardDetailsForm(forms.Form):
    YEAR_CHOICES = [(r, r) for r in range(1980, datetime.datetime.now().year + 1)]
    
    year = forms.ChoiceField(
        choices=YEAR_CHOICES, 
        initial=datetime.datetime.now().year,
        label='Année',
        widget=forms.Select(attrs={
            'class': 'form-control custom-select custom-select-sm',
            'style': 'max-width: 200px;'
        })
    )
    month = forms.ChoiceField(
        label='Mois',
        choices=[('', 'Tous les mois')] + list(Subscription.PLAN_CHOICES),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control custom-select custom-select-sm',
            'style': 'max-width: 200px;'
        })
    )
    bloc = forms.ChoiceField(
        label='Bloc',
        choices=[('', 'Tous les blocs')] + list(CustomUser.BLOC_CHOICES),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control custom-select custom-select-sm',
            'style': 'max-width: 200px;'
        })
    )
    export = forms.BooleanField(
        label='Exporter en CSV',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'custom-control-input',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'export':
                field.widget.attrs.update({
                    'class': 'form-control custom-select custom-select-sm',
                    'style': 'max-width: 200px;'
                })