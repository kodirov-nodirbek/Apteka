# Generated by Django 4.2.4 on 2023-11-09 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0020_alter_firmasavdolari_tolangan_summalar_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='harajat',
            name='hodim_id',
        ),
    ]