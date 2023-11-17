# Generated by Django 4.2.4 on 2023-11-17 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0027_alter_hisoblanganoylik_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='olinganoylik',
            old_name='summa',
            new_name='card_to_card',
        ),
        migrations.AddField(
            model_name='olinganoylik',
            name='naqd_pul',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=14),
            preserve_default=False,
        ),
    ]
