# Generated by Django 3.1.3 on 2021-01-16 09:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0052_auto_20210116_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='classification',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='code',
            field=models.CharField(max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 1, 15, 15, 27, 50, 820233)),
        ),
    ]
