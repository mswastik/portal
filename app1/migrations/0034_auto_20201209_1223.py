# Generated by Django 3.1.3 on 2020-12-09 06:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0033_auto_20201209_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bom',
            name='material_code',
            field=models.ManyToManyField(db_table='app1_bom_material_code', related_name='bom', to='app1.Material'),
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 8, 12, 23, 6, 904015)),
        ),
    ]
