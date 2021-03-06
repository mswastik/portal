# Generated by Django 3.1.3 on 2021-02-19 11:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0075_auto_20210216_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='wcgroup',
            name='cap',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 2, 18, 16, 46, 33, 573453)),
        ),
    ]