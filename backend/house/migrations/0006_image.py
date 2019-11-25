# Generated by Django 2.1.1 on 2019-11-12 08:37

from django.db import migrations, models
import django.db.models.deletion
import house.models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0005_auto_20191112_1403'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to=house.models.get_image_filename, verbose_name='Image')),
                ('seller_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house.SellerPost')),
            ],
        ),
    ]