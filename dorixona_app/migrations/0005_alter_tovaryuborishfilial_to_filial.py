# Generated by Django 4.2.4 on 2023-10-26 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0004_remove_tovaryuborishfilial_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tovaryuborishfilial',
            name='to_filial',
            field=models.PositiveIntegerField(),
        ),
    ]
