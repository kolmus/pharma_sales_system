# Generated by Django 3.2.9 on 2021-12-07 16:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manager_app', '0004_auto_20211207_1630'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Employee2',
            new_name='Employee',
        ),
    ]
