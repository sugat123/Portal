# Generated by Django 2.2.3 on 2019-08-26 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='job_type',
            field=models.CharField(max_length=55, null=True),
        ),
    ]
