# Generated by Django 3.1.3 on 2021-02-16 04:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0074_auto_20210216_1007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wcgroup',
            name='line',
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 2, 15, 10, 15, 54, 645707)),
        ),
    ]
