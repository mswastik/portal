# Generated by Django 3.1.3 on 2021-04-12 08:52

import datetime
from django.db import migrations, models
import month.models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0101_auto_20210412_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='forecast',
            name='month1',
            field=month.models.MonthField(default='2021-03'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 4, 11, 14, 21, 24, 611910)),
        ),
    ]
