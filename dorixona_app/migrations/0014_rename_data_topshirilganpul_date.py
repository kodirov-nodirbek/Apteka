# Generated by Django 4.2.4 on 2023-11-07 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0013_topshirilganpul_qabul_qilindi'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topshirilganpul',
            old_name='data',
            new_name='date',
        ),
    ]