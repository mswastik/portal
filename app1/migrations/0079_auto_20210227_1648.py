# Generated by Django 3.1.3 on 2021-02-27 11:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0078_auto_20210227_1638'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bom',
            old_name='bomversion',
            new_name='bom_version',
        ),
        migrations.AlterField(
            model_name='bom',
            name='ccode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bom_ccode', to='app1.material', verbose_name='component'),
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 2, 26, 16, 47, 52, 27760)),
        ),
    ]