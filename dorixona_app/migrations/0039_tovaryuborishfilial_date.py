# Generated by Django 4.2.4 on 2023-10-24 17:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0038_tovaryuborishfilial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tovaryuborishfilial',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
