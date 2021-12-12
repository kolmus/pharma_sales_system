from django.db import models
from manager_app.models import Employee, Branch

class Visit(models.Model):
    date = models.DateTimeField(verbose_name='Data wizyty', auto_now_add=True)
    visited = models.BooleanField(verbose_name='Wizyta wykonana', default=False)
    proof_img = models.ImageField(upload_to='static/img/client/visits/', verbose_name='Zdjęcie apteki')
    trader = models.ForeignKey(Employee, on_delete=models.PROTECT ,verbose_name="Handlowiec")
    client_branch = models.ForeignKey(Branch, on_delete=models.PROTECT, verbose_name="Klient")
    note = models.TextField(verbose_name="Notatka handlowca")

    def __str__(self):
        return f'{self.client_branch.name_of_branch} - {self.date}'