# Generated by Django 4.2.4 on 2024-01-04 12:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0039_remove_firmasavdolari_apteka_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='firmasavdolari',
            name='tolandi',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='kunliksavdo',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 4, 17, 2, 26, 628644)),
        ),
        migrations.AlterField(
            model_name='olinganoylik',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 4, 17, 2, 26, 628644)),
        ),
    ]
