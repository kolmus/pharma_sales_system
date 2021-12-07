from django import forms
from django.forms.widgets import PasswordInput
from .models import Employee

class LoginForm(forms.Form):
    """
    Creates form on Login page
    """    
    login = forms.CharField(label='Login')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)

class EmployeeAddForm (forms.Form):
    first_name = forms.CharField(label='Imię')
    last_name = forms.CharField(label='Nazwisko')
    username = forms.CharField(label='Nazwa użytkownia')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Numer telefonu')
    password1 = forms.CharField(label='Nowe hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz nowe hasło', widget=forms.PasswordInput, )
    role = forms.CharField(label='Stanowisko')
    supervisor = forms.ModelChoiceField(queryset=Employee.objects.all(), empty_label='supervisor', label='Przełożony', required=False)

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')
        if pass1 != pass2:
            raise forms.ValidationError('Hasła nie są takie same!')
        return cleaned_data


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(label='Wprowadź nowe hasło')
    new_password2 = forms.CharField(label='Powtórz nowe hasło')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('new_password')
        password_repeated = cleaned_data.get('new_password2')
        if password != password_repeated:
            raise forms.ValidationError('Hasła są różne!')
        return cleaned_data