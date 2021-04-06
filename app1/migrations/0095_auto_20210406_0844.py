# Generated by Django 3.1.3 on 2021-04-06 03:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0094_auto_20210405_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='fmodel',
            name='smape',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 4, 5, 8, 43, 59, 992219)),
        ),
    ]