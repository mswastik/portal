# Generated by Django 3.1.3 on 2020-12-01 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_auto_20201130_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='bom',
            name='bom_type',
            field=models.CharField(choices=[('FG', 'FG'), ('Bulk', 'Bulk')], default='FG', max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='so',
            name='remarks',
            field=models.CharField(default=1, max_length=45),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='line',
            name='prod_category',
            field=models.CharField(choices=[('Toothpaste', 'Toothpaste'), ('Toothpaste Pouch', 'Toothpaste Pouch'), ('Mouthwash', 'Mouthwash'), ('Toothpowder', 'Toothpowder'), ('Odonil', 'Odonil'), ('Bleach', 'Bleach'), ('Bleach Intermediate', 'Bleach Intermediate'), ('Odomos Lotion', 'Odomos Lotion'), ('HRC', 'HRC'), ('Petroleum Jelly', 'Petroleum Jelly'), ('Creamy PJ', 'Creamy PJ'), ('Handwash', 'Handwash'), ('Odomos', 'Odomos'), ('Denture Adhesive', 'Denture Adhesive'), ('Shaving Cream', 'Shaving Cream')], max_length=25),
        ),
    ]
