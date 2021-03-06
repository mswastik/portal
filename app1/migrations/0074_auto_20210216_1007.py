# Generated by Django 3.1.3 on 2021-02-16 04:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0073_auto_20210215_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 2, 15, 10, 7, 24, 664873)),
        ),
        migrations.CreateModel(
            name='Routing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.material')),
                ('wcgrp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.wcgroup')),
            ],
        ),
    ]
