# Generated by Django 3.1.3 on 2021-02-15 05:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0070_auto_20210214_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='capacity',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='line',
            name='uom',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 2, 14, 11, 20, 8, 296681)),
        ),
    ]
