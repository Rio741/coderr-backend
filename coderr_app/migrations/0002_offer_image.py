# Generated by Django 5.1.4 on 2025-01-11 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderr_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='offers/'),
        ),
    ]
