# Generated by Django 3.1.3 on 2020-12-01 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0022_auto_20201201_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='rate',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True),
        ),
    ]
