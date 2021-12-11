from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth.models import User
from datetime import date


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
    (1, 'Opłacona'),
    (2, 'Nieopłacona'),
    (3, 'Po terminie')
)
CLIENT_TYPE = (
    (1, 'Apteka sieciowa'),
    (2, 'Apteka rodzinna')
)

WEEKDAY = (
    (0, 'Poniedziałek'),
    (1, 'Wtorek'),
    (2, 'Środa'),
    (3, 'Czwartek'),
    (4, 'Piątek'),
    (5, 'Sobota'),
    (6, 'Niedziela')
)

ORDER_STATUS = (
    (0, 'Zamówienie w trakcie tworzenia.'),
    (1, 'Zamówienie przyjęte, oczekuje na weryfikację.'),
    (2, 'Zamówienie oczekuje na płatność'),
    (3, 'Potwierdzono zamówienie, przekazano do realizacji.'),
    (4, 'Skompletowane, oczekuje na kuriera.'),
    (5, 'Problem z zamówniem. Konieczność wyjaśnienia.'),
    (6, 'Przekazano kurierowi.'),
    (7, 'Oczekiwanie na płatność'),
    (8, 'Zakończone.')
)

class Employee(models.Model):
    phone = models.IntegerField(verbose_name="Numer telefonu")
    role = models.CharField(max_length=128, verbose_name='Stanowisko')
    supervisor = models.ForeignKey('Employee', verbose_name='Przełożony', on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    @property
    def name(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
    
    def __str__(self):
        return self.name


class Client(models.Model):
    nip = models.IntegerField(verbose_name='NIP')
    company_name = models.CharField(max_length=128, verbose_name='Nazwa firmy')
    logo = models.ImageField(upload_to='media/img/client/logo/', null=True)
    regon = models.IntegerField(verbose_name="REGON")
    krs = models.IntegerField(verbose_name="Numer KRS", null=True)
    type = models.IntegerField(choices=CLIENT_TYPE, verbose_name='Rodzaj apteki', default=2)
    
    def __str__(self):
        return self.company_name


class Branch(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Klient")
    type = models.IntegerField(choices=ADRESS_TYPES, verbose_name="rodzaj adresu")
    name_of_branch = models.CharField(max_length=60, verbose_name="Nazwa oddziału", null=True)
    zip_code = models.CharField(max_length=6, verbose_name='Kod pocztowy')
    province = models.CharField(max_length=16, verbose_name='Województwo', null=True)
    city = models.CharField(max_length=20, verbose_name='Miejscowość')
    street = models.CharField(max_length=64, verbose_name='Ulica')
    building_number = models.CharField(max_length=8, verbose_name='Numer budynku')
    apartment_number = models.CharField(max_length=8, verbose_name="Numer lokalu", null=True)
    details = models.TextField(verbose_name='Szczególne informacje', null=True)
    account_manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, verbose_name="Opiekun klienta", null=True)
    visit_days = models.IntegerField(choices=WEEKDAY, verbose_name="Wizyty w dni tygodnia")
    visit_hour_from = models.TimeField(auto_now=False, verbose_name='Wizyty od godziny', null=True, default='08:00')
    visit_hour_to = models.TimeField(auto_now=False, verbose_name="Wizyty do godziny", null=True, default ='16:00')
    
    def __str__(self):
        return f'{self.client} - {self.name_of_branch}'


class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name='Nazwa produktu')
    description = models.TextField(verbose_name='Opis', null=True)
    active_substance = models.CharField(max_length=64, verbose_name='Substancja czynna')
    is_active = models.BooleanField(default=True, verbose_name='W sprzedaży')
    
    def __str__(self):
        return self.name


class Variant(models.Model):
    dose = models.IntegerField(verbose_name="Dawka")
    unit = models.IntegerField(choices=UNITS, verbose_name="Jednostka(dawki)")
    in_package = models.IntegerField(verbose_name="Ilość w Opakowaniu")
    photo_main = models.ImageField(upload_to='img/products/', verbose_name="Zdjęcie główne", null=True)
    photo_2 = models.ImageField(upload_to='media/img/products/', verbose_name="Zdjęcie 2", null=True)
    photo_3 = models.ImageField(upload_to='media/img/products/', verbose_name="Zdjęcie 3", null=True)
    photo_4 = models.ImageField(upload_to='media/img/products/', verbose_name="Zdjęcie 4", null=True)
    photo_5 = models.ImageField(upload_to='media/img/products/', verbose_name="Zdjęcie 5", null=True)
    photo_6 = models.ImageField(upload_to='media/img/products/', verbose_name="Zdjęcie 6", null=True)
    photo_7 = models.ImageField(upload_to='media/img/products/', verbose_name="Zdjęcie 7", null=True)
    photo_8 = models.ImageField(upload_to='media/img/products/', verbose_name="Zdjęcie 8", null=True)
    photo_9 = models.ImageField(upload_to='media/img/products/', verbose_name="Zdjęcie 9", null=True)
    photo_10 = models.ImageField(upload_to='media/img/products/', verbose_name="Zdjęcie 10", null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name= "Produkt")
    next_delivery = models.DateField(null=True, verbose_name="Planowana data następnej dostawy")
    is_active = models.BooleanField(default=True, verbose_name='W sprzedaży')
    
    def __str__(self):
        stock = 0
        for n in self.batch_set.all():
            stock += n.quantity
        return f'{self.product.name}, Dawka {self.dose}{self.get_unit_display()}, {self.in_package}szt, Stock: {stock}'


class Batch(models.Model):
    number = models.CharField(max_length=32, verbose_name="numer Partii")
    ean = models.IntegerField(verbose_name='EAN')
    expiration_date = models.DateField(verbose_name="data Przydatności do użycia")
    netto = models.FloatField(verbose_name="cena netto")
    vat = models.IntegerField(choices=VAT, verbose_name='Starka podatku vat')
    quantity = models.IntegerField(verbose_name='Ilość produktów')
    variant = models.ForeignKey(Variant, on_delete=CASCADE, verbose_name='Produkt')
    is_active = models.BooleanField(default=True, verbose_name="W sprzedaży")
    
    def brutto(self):
        return str(float(self.netto) * (float(self.vat) + 1))
    
    def __str__(self):
        return self.number


class Invoice(models.Model):
    number = models.CharField(max_length=32, verbose_name='Numer Faktury')
    date = models.DateField(auto_now=True, verbose_name='Data wystawienia')
    status = models.IntegerField(choices=PAYMENT_STATUS, verbose_name='Status płatności')
    payment_date = models.DateField(verbose_name='Termin płatności')
    
    def __str__(self):
        return self.number


class Order(models.Model):
    order_number = models.CharField(max_length=32, verbose_name='Numer zamówienia')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, verbose_name="Klient")
    batch = models.ManyToManyField(Batch, verbose_name='Pozycje', related_name='order', through='Cart')
    invoice = models.ForeignKey(Invoice, on_delete=SET_NULL, null=True, verbose_name="Faktura")
    discount = models.IntegerField(verbose_name='Zniżka', default=0)
    order_status = models.IntegerField(choices=ORDER_STATUS, verbose_name='Status zamówienia', default=0)
    date = models.DateField(auto_now=True, null=True)
    
    def __str__(self):
        return f'{self.order_number} - {self.branch}'
    
    def total_netto(self):
        result = 0
        for position in self.cart_set.all():
            result += float(position.batch.netto) * position.quantity
        return result
    
    def total_brutto(self):
        result = 0
        for position in self.cart_set.all():
            result += (float(position.batch.netto) * position.quantity) * (1 + float(position.batch.get_vat_display()))
        return result


class Visit(models.Model):
    date = models.DateTimeField(verbose_name='Data wizyty', auto_now_add=True)
    visited = models.BooleanField(verbose_name='Wizyta wykonana', default=False)
    proof_img = models.ImageField(upload_to='static/img/client/visits/', verbose_name='Zdjęcie apteki')
    trader = models.ForeignKey(Employee, on_delete=models.PROTECT ,verbose_name="Handlowiec")
    client_branch = models.ForeignKey(Branch, on_delete=models.PROTECT, verbose_name="Klient")
    note = models.TextField(verbose_name="Notatka handlowca")


class Cart(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Zamówienie')
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, verbose_name='Produkt i wariant')
    quantity = models.IntegerField(verbose_name='Ilość')
    
    def total_netto(self):
        result = float(self.batch.netto) * self.quantity
        return result
    
    def total_brutto(self):
        total_netto = float(self.batch.netto) * self.quantity
        result = round(total_netto * (1 + float(self.batch.get_vat_display())), 2)
        return result


class CalendarSupervisor(models.Model):
    owner = models.ForeignKey(Employee, verbose_name='Właściciel', on_delete=models.PROTECT, related_name="calendar_supervisor")
    date = models.DateField(verbose_name='Data spotkania', )
    employee = models.ForeignKey(Employee, null=True, verbose_name="Podopieczny", on_delete=models.PROTECT)
    note = models.TextField(verbose_name="Notatka")
    
    
    def __str__(self):
        year, month, day = (int(x) for x in self.date.split('-'))
        return f'Data: {self.date}, {date(year=year, month=month, day=day).weekday()}'
