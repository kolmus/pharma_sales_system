from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import CharField, IntegerField
from django.db.models.fields.related import ForeignKey

ADRESS_TYPES = (
    (1, 'Adres korespondencyjny'),
    (2, 'Adres Rejestracyjny'),
)
UNITS = (
    (1, 'mg'),
    (2, 'ml')
)

VAT = (
    (1, '0.08'),
    (2, '0.23')
)
PAYMENT_STATUS = (
    (1, 'Opłacona')
    (2, 'Nieopłacona')
    (3, 'Po terminie')
)

class Employee(models.Model):
    first_name = models.CharField(max_length=64, verbose_name="Imię: ")
    last_name = models.CharField(max_length=64, verbose_name="Nazwisko: ")
    phone = models.IntegerField(verbose_name="Numer telefonu: ")
    email = models.CharField(max_length=80, verbose_name="Eadres e-mail: ")
    role = models.CharField(max_length=128, verbose_name='Stanowisko: ')
    supervisor = models.ForeignKey('Employee', verbose_name='Przełożony: ', on_delete=models.SET_NULL)
    is_active = models.BooleanField(verbose_name='Aktywny: ', default=True)
    
    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)
    
    def __str__(self):
        return self.name



class Client(models.Model):
    company_name = models.CharField(max_length=128, verbose_name='Nazwa firmy: ')
    logo = models.ImageField(upload_to='img/client/logo/', null=True)
    nip = models.IntegerField(verbose_name='NIP: ')
    regon = models.IntegerField(verbose_name="REGON: ")
    krs = models.IntegerField(verbose_name="Numer KRS = ", null=True)
    account_manager = models,ForeignKey(Employee, verbose_name="Opiekun klienta")
    
    def __str__(self):
        return self.company_name
    
class Adress(models.Model):
    city = models.CharField(max_length=20, verbose_name='Miejscowość; ')
    street = models.CharField(max_length=64, verbose_name='Ulica: ')
    building_number = models.CharField(max_length=8, verbose_name='Numer budynku: ')
    apartment_number = models.CharField(max_length=8, verbose_name="Numer lokalu: ", null=True)
    zip_code = models.CharField(max_length=6, verbose_name='Kod pocztowy')
    type = models.IntegerField(choices=ADRESS_TYPES, verbose_name="rodzaj adresu")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Klient: ")
    
    def __str__(self):
        return '{} {}/{}, {} {}'.format(self.street, self.building_number, self.apartment_number, self.zip_code, self.city)
    
class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name='Nazwa produktu')
    description = models.TextField(verbose_name='Opis: ', null=True)
    active_substance = models.CharField(max_length=64, verbose_name='Substancja czynna')
    
    def __str__(self):
        return self.name
    
    
class Variant(models.Model):
    dose = IntegerField(verbose_name="Dawka: ")
    unit = IntegerField(choices=UNITS, verbose_name="Jednostka(dawki): ")
    in_package = IntegerField(verbose_name="Ilość w Opakowaniu")
    photo_main = models.ImageField(upload_to='img/products/', verbose_name="Zdjęcie główne: ")
    photo_2 = models.ImageField(upload_to='img/products/', verbose_name="Zdjęcie 2: ", null=True)
    photo_3 = models.ImageField(upload_to='img/products/', verbose_name="Zdjęcie 3: ", null=True)
    photo_4 = models.ImageField(upload_to='img/products/', verbose_name="Zdjęcie 4: ", null=True)
    photo_5 = models.ImageField(upload_to='img/products/', verbose_name="Zdjęcie 5: ", null=True)
    photo_6 = models.ImageField(upload_to='img/products/', verbose_name="Zdjęcie 6: ", null=True)
    photo_7 = models.ImageField(upload_to='img/products/', verbose_name="Zdjęcie 7: ", null=True)
    photo_8 = models.ImageField(upload_to='img/products/', verbose_name="Zdjęcie 8: ", null=True)
    photo_9 = models.ImageField(upload_to='img/products/', verbose_name="Zdjęcie 9: ", null=True)
    photo_10 = models.ImageField(upload_to='img/products/', verbose_name="Zdjęcie 10: ", null=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name= "Produkt: ")
    next_delivery = models.DateField(null=True, verbose_name="Planowana data następnej dostawy: ")
    
    def __str__(self):
        return f'Dawka {self.dose}{self.unit}'
    
    
class Batch(models.Model):
    number = models.CharField(max_length=8, verbose_name="numer Partii: ")
    ean = models.IntegerField(verbose_name='EAN: ')
    expiration_date = models.DateField(verbose_name="data Przydatności do użycia: ")
    netto = models.FloatField(verbose_name="cena netto: ")
    vat = IntegerField(choices=VAT, verbose_name='Starka podatku vat: ')
    quantity = IntegerField(verbose_name='Ilość produktów: ')
    variant = ForeignKey(Variant, on_delete=CASCADE, verbose_name='Produkt: ')
    
    def __str__(self):
        return self.number
    
    
class Invoice(models.Model):
    number = models.CharField(max_length=32, verbose_name='Numer Faktury: ')
    date = models.DateField(auto_now=True, verbose_name='Data wystawienia: ')
    status = models.IntegerField(choces=PAYMENT_STATUS, verbose_name='Status płatności: ')
    payment_date = models.DateField(verbose_name='Termin płatności: ')
    
    def __str__(self):
        return self.number
    
    
class Order(models.Model):
    order_number = models.CharField(max_length=32, verbose_name='Numer zamówienia: ')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Klient: ")
    variant = models.ManyToManyField(Variant, verbose_name='Pozycje: ', related_name='Order: ')
    invoice = models.ForeignKey(Invoice, on_delete=SET_NULL, null=True, verbose_name="Faktura: ")
    order_quantity = IntegerField(verbose_name='Ilość: ')
    discount = models.IntegerField(verbose_name='Zniżka: ')
    
    def __str__(self):
        return self.order_number
    
    

