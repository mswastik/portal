# Generated by Django 3.1.3 on 2020-12-01 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_auto_20201201_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='bulk_code',
            field=models.CharField(max_length=7, null=True),
        ),
    ]
