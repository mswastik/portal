# Generated by Django 3.1.3 on 2020-11-30 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_auto_20201129_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='plant',
            field=models.CharField(choices=[('1024', '1024'), ('1025', '1025')], default='1024', max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='line',
            name='prod_category',
            field=models.CharField(choices=[('Toothpaste', 'Toothpaste'), ('Toothpaste Pouch', 'Toothpaste Pouch'), ('Mouthwash', 'Mouthwash'), ('Toothpowder', 'Toothpowder'), ('Odonil', 'Odonil'), ('Bleach', 'Bleach'), ('Odomos Lotion', 'Odomos Lotion'), ('HRC', 'HRC'), ('Petroleum Jelly', 'Petroleum Jelly'), ('Creamy PJ', 'Creamy PJ'), ('Handwash', 'Handwash'), ('Odomos', 'Odomos')], default='Toothpaste', max_length=25),
            preserve_default=False,
        ),
    ]
