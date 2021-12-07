# Generated by Django 3.2.9 on 2021-12-07 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manager_app', '0003_auto_20211206_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variant',
            name='photo_2',
            field=models.ImageField(null=True, upload_to='static/img/products/', verbose_name='Zdjęcie 2: '),
        ),
        migrations.CreateModel(
            name='Employee2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.IntegerField(verbose_name='Numer telefonu: ')),
                ('role', models.CharField(max_length=128, verbose_name='Stanowisko: ')),
                ('supervisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='manager_app.employee2', verbose_name='Przełożony: ')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='visit',
            name='trader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='manager_app.employee2', verbose_name='Handlowiec: '),
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
    ]
