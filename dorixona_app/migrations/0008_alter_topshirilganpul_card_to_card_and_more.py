# Generated by Django 4.2.4 on 2023-10-26 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0007_alter_topshirilganpul_card_to_card_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topshirilganpul',
            name='card_to_card',
            field=models.DecimalField(decimal_places=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='topshirilganpul',
            name='naqd_pul',
            field=models.DecimalField(decimal_places=0, max_digits=14),
        ),
    ]
