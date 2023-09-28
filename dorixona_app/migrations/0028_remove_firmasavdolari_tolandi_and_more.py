# Generated by Django 4.2.4 on 2023-09-23 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0027_remove_firmasavdolari_firmaga_qaytarildi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='firmasavdolari',
            name='tolandi',
        ),
        migrations.AlterField(
            model_name='firmasavdolari',
            name='qaytarilgan_tovar_summasi',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=14),
        ),
    ]