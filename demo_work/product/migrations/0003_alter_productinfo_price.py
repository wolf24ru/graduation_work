# Generated by Django 4.0.4 on 2022-05-10 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_productparameter_parameter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinfo',
            name='price',
            field=models.FloatField(verbose_name='Price'),
        ),
    ]
