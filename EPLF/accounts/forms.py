# # accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput
from phonenumber_field.formfields import PhoneNumberField
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email","address","feecharge")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email","address","feecharge")




class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control form-control-user',
                                                       'placeholder': 'Enter username...'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control form-control-user',
                                                           'placeholder': 'Password'}))


class EditProfileForm(UserChangeForm):
    first_name = forms.CharField(label="First Name", widget=TextInput(attrs={'class': 'form-control form-control-user'}),
                                 required=False)

    last_name = forms.CharField(label="Last Name", widget=TextInput(attrs={'class': 'form-control form-control-user'}),
                                required=False)

    username = forms.CharField(label="Username", widget=TextInput(attrs={'class': 'form-control form-control-user'}))
    email = forms.EmailField(label="Email", widget=TextInput(attrs={'class': 'form-control form-control-user'}))

    password = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
                raise forms.ValidationError('Email already exists')
        return email

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password",
                                   widget=PasswordInput(attrs={'class': 'form-control form-control-user'}))

    new_password1 = forms.CharField(label="New Password",
                                    widget=PasswordInput(attrs={'class': 'form-control form-control-user'}))

    new_password2 = forms.CharField(label="Confirm Password",
                                    widget=PasswordInput(attrs={'class': 'form-control form-control-user'}))


class CreateuserForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur", widget=TextInput(attrs={'class': 'form-control form-control-user'}))
    first_name = forms.CharField(label="Prénom", widget=TextInput(attrs={'class': 'form-control form-control-user'}),
                                 required=False)

    last_name = forms.CharField(label="Nom", widget=TextInput(attrs={'class': 'form-control form-control-user'}),
                                required=False)

    email = forms.EmailField(label="Email", widget=TextInput(attrs={'class': 'form-control form-control-user'}))
    address = forms.CharField(max_length=200, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '3'
    }))
    phone_number = PhoneNumberField(region="DZ", widget=TextInput(attrs={'class': 'form-control form-control-user'}), label="Numéro de Téléphone")

    feecharge = forms.DecimalField(label="Charge", widget=TextInput(attrs={'class': 'form-control form-control-user'}))

    class Meta:
        model = CustomUser
        fields = ["username",'first_name', 'last_name', 'email', 'address', 'phone_number',"feecharge"]
