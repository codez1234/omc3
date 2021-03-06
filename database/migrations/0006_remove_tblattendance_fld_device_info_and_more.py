# Generated by Django 4.0.3 on 2022-05-24 07:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_alter_tblrates_fld_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tblattendance',
            name='fld_device_info',
        ),
        migrations.AlterField(
            model_name='tblattendance',
            name='fld_latitude',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)]),
        ),
        migrations.AlterField(
            model_name='tblattendance',
            name='fld_longitude',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)]),
        ),
    ]
