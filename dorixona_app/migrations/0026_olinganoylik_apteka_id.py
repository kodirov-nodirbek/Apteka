# Generated by Django 4.2.4 on 2023-11-12 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0025_rename_hodim_hisoblanganoylik_hodim_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='olinganoylik',
            name='apteka_id',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]