# Generated by Django 3.1.3 on 2020-12-09 06:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0032_auto_20201207_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bom',
            name='material_code',
            field=models.ManyToManyField(db_table='app1_bom_material_code', related_name='material', to='app1.Material'),
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 8, 12, 21, 32, 37177)),
        ),
    ]
