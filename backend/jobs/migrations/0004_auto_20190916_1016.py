# Generated by Django 2.2.3 on 2019-09-16 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20190912_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliedjob',
            name='skills',
            field=models.ManyToManyField(to='jobs.Skills'),
        ),
        migrations.AlterField(
            model_name='postedjob',
            name='skills',
            field=models.ManyToManyField(to='jobs.Skills'),
        ),
    ]
