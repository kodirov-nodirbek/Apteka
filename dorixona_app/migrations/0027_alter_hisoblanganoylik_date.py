# Generated by Django 4.2.4 on 2023-11-14 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0026_olinganoylik_apteka_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hisoblanganoylik',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
