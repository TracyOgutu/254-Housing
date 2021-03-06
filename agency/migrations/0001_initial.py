# Generated by Django 2.2 on 2021-08-15 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('housename', models.CharField(max_length=100)),
                ('house_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('description', tinymce.models.HTMLField(blank=True, null=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(null=True)),
                ('image', models.ImageField(default='profile/default.png', upload_to='profile')),
                ('buyer', models.BooleanField(default=False)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('interestedin', models.CharField(blank=True, max_length=200)),
                ('firstname', models.CharField(blank=True, max_length=30)),
                ('lastname', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
