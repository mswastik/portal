# Generated by Django 3.1.3 on 2021-01-15 15:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0044_auto_20210101_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 1, 14, 20, 59, 52, 834407)),
        ),
    ]
