# Generated by Django 4.2.4 on 2023-11-09 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0021_remove_harajat_hodim_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='harajat',
            name='firma_uchun',
            field=models.BooleanField(default=False),
        ),
    ]
