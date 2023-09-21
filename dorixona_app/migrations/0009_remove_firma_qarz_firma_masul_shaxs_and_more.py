# Generated by Django 4.2.4 on 2023-09-16 16:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dorixona_app', '0008_nasiya_tolov_tarixi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='firma',
            name='qarz',
        ),
        migrations.AddField(
            model_name='firma',
            name='masul_shaxs',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='firma',
            name='yaqin_qaytarish_sanasi',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='FirmaSavdolari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('harid_sanasi', models.DateTimeField(auto_now=True)),
                ('tovar_summasi', models.DecimalField(decimal_places=2, max_digits=11)),
                ('tolangan_summalar', models.JSONField(default=dict)),
                ('firma_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dorixona_app.firma')),
            ],
        ),
    ]
