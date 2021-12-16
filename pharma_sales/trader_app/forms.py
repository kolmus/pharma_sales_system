from django import forms


from manager_app.models import ADRESS_TYPES, CLIENT_TYPE, WEEKDAY
from .models import Visit

class PlanDateForm(forms.Form):
    plan_date = forms.DateField(widget=forms.SelectDateWidget, label='Jaki dzień chcesz planować?', required=False)
    city = forms.CharField(label='Wprowadź miejscowość',)
    
class PlanAddVisitForm(forms.Form):
    
    branch = forms.ModelChoiceField(queryset=None, label=None)
        
class MakeVisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['proof_img', 'note']


class ClientByNipForm(forms.Form):
    nip = forms.IntegerField(label="NIP")
    company_name = forms.CharField(max_length=128, label="Nazwa firmy")
    short_company_name = forms.CharField(max_length=16, label='Skrócona nazwa')
    logo = forms.ImageField(label="Logo", required=False)
    regon = forms.IntegerField(label="REGON")
    krs = forms.IntegerField(label="KRS", required=False)
    type = forms.ChoiceField(choices=CLIENT_TYPE, label="Rodzaj Klienta")
    name_of_branch = forms.CharField(max_length=60, label="Nazwa oddziału")
    zip_code = forms.CharField(label="Kod pocztowy", max_length=6)
    province = forms.CharField(max_length=16, label="Województwo", required=False)
    city = forms.CharField(max_length=20, label="Miejscowość")
    street = forms.CharField(max_length=64, label="Ulica")
    building_number = forms.CharField(max_length=8, label="Numer budynku")
    apartment_number = forms.CharField(max_length=8, label="Numer lokalu", required=False)
    details = forms.CharField(label="Szczególne informacje", widget=forms.Textarea, required=False)
    visit_days = forms.ChoiceField(choices=WEEKDAY, label="Wizyty w dni tygodnia")
    visit_hour_from = forms.TimeField(label="Wizyty od godziny", required=False)
    visit_hour_to = forms.TimeField(label="wizyty do godziny", required=False)
    
    