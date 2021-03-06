# Generated by Django 3.1.3 on 2021-02-14 16:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0067_auto_20210214_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='bom',
            name='ccode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bom_ccode', to='app1.material', verbose_name='component'),
        ),
        migrations.AlterField(
            model_name='bom',
            name='code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.material'),
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 2, 13, 21, 53, 54, 96718)),
        ),
    ]