# Generated by Django 3.0.1 on 2020-11-03 23:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hard_tacks_education_system', '0010_auto_20201104_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkededucationtask',
            name='solution_time',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='Время, когда принято решение'),
        ),
    ]
