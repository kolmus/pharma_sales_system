# Generated by Django 3.2.9 on 2021-12-12 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='note',
            field=models.TextField(null=True, verbose_name='Notatka handlowca'),
        ),
        migrations.AlterField(
            model_name='visit',
            name='proof_img',
            field=models.ImageField(null=True, upload_to='static/img/client/visits/', verbose_name='Zdjęcie apteki'),
        ),
    ]
