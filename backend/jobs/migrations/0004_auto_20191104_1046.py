# Generated by Django 2.2.3 on 2019-11-04 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20191104_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='job_type',
            field=models.IntegerField(null=True),
        ),
    ]
