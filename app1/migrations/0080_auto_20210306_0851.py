# Generated by Django 3.1.3 on 2021-03-06 03:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0079_auto_20210227_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 3, 5, 8, 51, 12, 458223)),
        ),
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField(default=datetime.datetime.now)),
                ('version', models.IntegerField()),
                ('qty', models.DecimalField(decimal_places=2, max_digits=7)),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.material')),
            ],
        ),
    ]
