# Generated by Django 4.2.4 on 2023-09-17 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0019_alter_firmasavdolari_tolash_sanasi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='firma',
            name='eng_yaqin_tolov_sanasi',
        ),
    ]
