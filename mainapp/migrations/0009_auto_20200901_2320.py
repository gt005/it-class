# Generated by Django 3.0.1 on 2020-09-01 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20200901_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketproduct',
            name='product_size',
            field=models.CharField(default='Стандарт', max_length=200, verbose_name='Размер или краткое описание товара'),
        ),
    ]
