# Generated by Django 4.2.4 on 2023-10-25 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0002_alter_apteka_jami_qoldiq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tovaryuborishfilial',
            name='from_filial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='from_fil', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tovaryuborishfilial',
            name='to_filial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='to_fil', to=settings.AUTH_USER_MODEL),
        ),
    ]