
from django.db import models
from manager_app.models import Employee, Branch


class Visit(models.Model):
    date = models.DateTimeField(verbose_name='Data wizyty', )
    visited = models.BooleanField(verbose_name='Wizyta wykonana', default=False)
    proof_img = models.ImageField(upload_to='media/img/client/visits/', verbose_name='Zdjęcie apteki', null=True)
    trader = models.ForeignKey(Employee, on_delete=models.PROTECT ,verbose_name="Handlowiec")
    client_branch = models.ForeignKey(Branch, on_delete=models.PROTECT, verbose_name="Klient")
    note = models.TextField(verbose_name="Notatka handlowca", null=True)

    def __str__(self):
        return f'{self.client_branch.name_of_branch} - {self.date}'


class Localization(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    latitude = models.FloatField(null = True)
    longitude = models.FloatField(null = True)
    note = models.CharField(max_length=256)
    