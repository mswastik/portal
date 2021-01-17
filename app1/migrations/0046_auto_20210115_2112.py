# Generated by Django 3.1.3 on 2021-01-15 15:42

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0045_auto_20210115_2100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bom',
            name='material_code',
        ),
        migrations.AddField(
            model_name='bom',
            name='material_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bom', to='app1.material'),
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 1, 14, 21, 12, 11, 961200)),
        ),
    ]
