# Generated by Django 4.2.4 on 2023-09-21 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0022_alter_firmasavdolari_tolov_muddati'),
    ]

    operations = [
        migrations.AddField(
            model_name='nasiya',
            name='apteka_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dorixona_app.apteka'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nasiyachi',
            name='apteka_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dorixona_app.apteka'),
            preserve_default=False,
        ),
    ]
