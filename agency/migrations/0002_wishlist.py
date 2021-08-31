# Generated by Django 2.2 on 2021-08-30 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_mac', models.CharField(max_length=1000)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agency.House')),
            ],
        ),
    ]