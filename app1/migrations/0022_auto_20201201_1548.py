# Generated by Django 3.1.3 on 2020-12-01 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0021_auto_20201201_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='desc',
            field=models.CharField(max_length=45),
        ),
    ]
