# Generated by Django 3.1.3 on 2021-04-12 08:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0103_auto_20210412_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 4, 11, 14, 27, 5, 562534)),
        ),
    ]
