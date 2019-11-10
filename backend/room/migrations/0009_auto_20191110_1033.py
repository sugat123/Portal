# Generated by Django 2.2.3 on 2019-11-10 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0008_postedroom_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postedroom',
            name='conditon',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='postedroom',
            name='facility',
            field=models.ManyToManyField(to='room.Facility'),
        ),
    ]
