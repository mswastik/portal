# Generated by Django 3.1.3 on 2021-04-06 03:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0097_auto_20210406_0848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forecast',
            name='dem_month1',
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 4, 5, 8, 51, 49, 507542)),
        ),
    ]