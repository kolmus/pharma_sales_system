# Generated by Django 3.2.9 on 2021-12-10 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0003_auto_20211210_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='visit_days',
            field=models.IntegerField(choices=[(0, 'Poniedziałek'), (1, 'Wtorek'), (2, 'Środa'), (3, 'Czwartek'), (4, 'Piątek'), (5, 'Sobota'), (6, 'Niedziela')], verbose_name='Wizyty w dni tygodnia'),
        ),
        migrations.CreateModel(
            name='CalendarSupervisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Data spotkania')),
                ('note', models.TextField(verbose_name='Notatka')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='manager_app.employee', verbose_name='Podopieczny')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='calendar_supervisor', to='manager_app.employee', verbose_name='Właściciel')),
            ],
        ),
    ]
