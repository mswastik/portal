# Generated by Django 3.1.3 on 2021-03-08 06:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0085_auto_20210308_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.material'),
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 3, 7, 11, 39, 0, 52993)),
        ),
    ]
