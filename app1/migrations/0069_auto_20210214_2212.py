# Generated by Django 3.1.3 on 2021-02-14 16:42

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0068_auto_20210214_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 2, 13, 22, 12, 1, 585439)),
        ),
        migrations.AlterField(
            model_name='speed',
            name='code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.material', to_field='code'),
        ),
    ]
