# Generated by Django 3.2.9 on 2021-12-08 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0008_auto_20211208_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='province',
            field=models.CharField(max_length=16, null=True, verbose_name='Województwo'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='city',
            field=models.CharField(max_length=20, verbose_name='Miejscowość'),
        ),
    ]