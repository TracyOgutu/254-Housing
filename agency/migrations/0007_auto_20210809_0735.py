# Generated by Django 2.2 on 2021-08-09 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0006_auto_20210809_0653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='interestedin',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
