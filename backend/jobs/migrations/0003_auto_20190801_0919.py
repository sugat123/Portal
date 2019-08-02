# Generated by Django 2.2.3 on 2019-08-01 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_appliedjob_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facility',
            old_name='title',
            new_name='other',
        ),
        migrations.AddField(
            model_name='facility',
            name='salary',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='working_time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
