# Generated by Django 3.1.3 on 2021-04-20 08:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0106_auto_20210418_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='fore_qty',
            field=models.DecimalField(decimal_places=2, max_digits=11),
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 4, 19, 14, 28, 33, 59103)),
        ),
    ]
