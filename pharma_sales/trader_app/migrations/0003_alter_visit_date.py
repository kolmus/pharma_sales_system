# Generated by Django 3.2.9 on 2021-12-12 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader_app', '0002_auto_20211212_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='date',
            field=models.DateTimeField(verbose_name='Data wizyty'),
        ),
    ]