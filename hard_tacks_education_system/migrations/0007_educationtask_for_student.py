# Generated by Django 3.0.1 on 2020-11-03 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_auto_20201101_2341'),
        ('hard_tacks_education_system', '0006_auto_20201101_0212'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationtask',
            name='for_student',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Puples', verbose_name='Предназначена для этого ученика'),
        ),
    ]
