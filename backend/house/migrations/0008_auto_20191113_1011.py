# Generated by Django 2.1.1 on 2019-11-13 04:26

from django.db import migrations, models
import house.models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0007_auto_20191112_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=house.models.get_image_filename, verbose_name='Image'),
        ),
    ]
