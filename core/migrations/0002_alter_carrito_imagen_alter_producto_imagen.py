# Generated by Django 4.0.4 on 2024-07-15 03:08

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrito',
            name='imagen',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='imagen'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=cloudinary.models.CloudinaryField(default=1, max_length=255, verbose_name='imagen'),
            preserve_default=False,
        ),
    ]
