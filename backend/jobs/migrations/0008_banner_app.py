# Generated by Django 2.2.3 on 2019-08-07 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_auto_20190807_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='app',
            field=models.ImageField(default='default.jpg', upload_to='banner'),
        ),
    ]
