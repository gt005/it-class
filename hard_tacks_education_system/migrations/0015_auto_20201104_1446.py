# Generated by Django 3.0.1 on 2020-11-04 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hard_tacks_education_system', '0014_auto_20201104_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkededucationtask',
            name='solution_time',
            field=models.DateTimeField(verbose_name='Время, когда принято решение'),
        ),
    ]