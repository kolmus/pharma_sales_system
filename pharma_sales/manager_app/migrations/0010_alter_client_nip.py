# Generated by Django 3.2.9 on 2021-12-15 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0009_alter_branch_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='nip',
            field=models.BigIntegerField(verbose_name='NIP'),
        ),
    ]
