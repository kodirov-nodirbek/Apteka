# Generated by Django 4.2.4 on 2024-01-02 06:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0037_alter_olinganoylik_card_to_card_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kunliksavdo',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 2, 11, 13, 26, 37115)),
        ),
        migrations.AlterField(
            model_name='olinganoylik',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 2, 11, 13, 26, 37115)),
        ),
    ]
