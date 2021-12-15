from django import forms
from .models import UNITS, Batch, Client, Employee, Product, Variant


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
    phone = forms.IntegerField(label='Numer telefonu')
    password1 = forms.CharField(label='Nowe hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz nowe hasło', widget=forms.PasswordInput, )
    role = forms.CharField(label='Stanowisko')
    supervisor = forms.ModelChoiceField(queryset=Employee.objects.filter(is_supervisor=True), empty_label='supervisor', label='Przełożony', required=False)

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')
        if pass1 != pass2:
            raise forms.ValidationError('Hasła nie są takie same!')
        if not pass1 or not pass2:
            raise forms.ValidationError('hasła nie mogą być puste')
        return cleaned_data


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(label='Wprowadź nowe hasło', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Powtórz nowe hasło', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('new_password')
        password_repeated = cleaned_data.get('new_password2')
        if password != password_repeated:
            raise forms.ValidationError('Hasła są różne!')
        return cleaned_data


class EmployeeEditForm(forms.Form):
    first_name = forms.CharField(label='Imię')
    last_name = forms.CharField(label='Nazwisko')
    email = forms.EmailField(label='Email')
    phone = forms.IntegerField(label='Numer telefonu')
    role = forms.CharField(label='Stanowisko')
    supervisor = forms.ModelChoiceField(queryset=Employee.objects.filter(is_supervisor=True), empty_label='supervisor', label='Przełożony', required=False)
    

class ClientForm(forms.ModelForm):
    # logo = forms.ImageField(required=False)
    krs = forms.IntegerField(required=False)
    class Meta:
        model = Client
        fields = ['nip', 'company_name', 'logo', 'regon', 'krs', 'type']
        

class VariantForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Produkt główny')
    dose = forms.IntegerField(label='Dawka (ilość)')
    unit = forms.ChoiceField(choices=UNITS, label = 'Dawka(jednostka)')
    in_package = forms.IntegerField(label='Ilość w pakiecie')
    next_delivery = forms.DateField(label='Planowana dostawa', required=False)
    photo_main = forms.ImageField(label='Zdjęcie główne', required=False)
    photo2 = forms.ImageField(label='Zdjęcie2', required=False)
    photo3 = forms.ImageField(label='Zdjęcie3', required=False)
    photo4 = forms.ImageField(label='Zdjęcie4', required=False)
    photo5 = forms.ImageField(label='Zdjęcie5', required=False)
    photo6 = forms.ImageField(label='Zdjęcie6', required=False)
    photo7 = forms.ImageField(label='Zdjęcie7', required=False)
    photo8 = forms.ImageField(label='Zdjęcie8', required=False)
    photo9 = forms.ImageField(label='Zdjęcie9', required=False)
    photo10 = forms.ImageField(label='Zdjęcie10', required=False)
    
    
class CartForm(forms.Form):
    variant = forms.ModelChoiceField(queryset = Variant.objects.filter(is_active=True).order_by('dose'), empty_label='Wybierz produkt', label="Wybierz produkt")
    quantity = forms.IntegerField(label='Podaj ilość paczek')
    
    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        variant = cleaned_data.get('variant')
        stock = 0
        for batch in variant.batch_set.filter(is_active=True):
            stock += batch.quantity
        if quantity > 0 and quantity < stock:
            return cleaned_data
        else:
            raise forms.ValidationError('Ilość mniejsza niż 0 lub większa niż stan magazynowy')
        

class CalendarForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=None, label=False, required=False)
    note = forms.CharField(label=False, widget=forms.Textarea(attrs={'placeholder': 'Notatka z dnia'}), required=False)
    

