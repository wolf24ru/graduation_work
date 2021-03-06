# Generated by Django 4.0.4 on 2022-04-21 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, verbose_name='city')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': "City's list",
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=150, verbose_name='region')),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': "Region's list",
            },
        ),
        migrations.CreateModel(
            name='RegionCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_rc', to='location.city', verbose_name='City')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='region_rc', to='location.region', verbose_name='Region')),
            ],
        ),
    ]
