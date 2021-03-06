# Generated by Django 3.1.3 on 2021-02-14 10:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0058_auto_20210214_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='code',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 2, 13, 15, 57, 33, 336607)),
        ),
    ]
