from typing_extensions import Required
from django import forms

from datetime import date
from .models import Visit

class PlanDateForm(forms.Form):
    plan_date = forms.DateField(widget=forms.SelectDateWidget, label='Jaki dzień chcesz planować?', required=False)
    city = forms.CharField(label='Wprowadź miejscowość', required=False)
    
class PlanAddVisitForm(forms.Form):
    
    branch = forms.ModelChoiceField(queryset=None, label=None)
        