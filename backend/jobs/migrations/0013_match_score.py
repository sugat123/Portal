# Generated by Django 2.2.3 on 2019-08-16 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0012_auto_20190814_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='score',
            field=models.FloatField(null=True),
        ),
    ]
