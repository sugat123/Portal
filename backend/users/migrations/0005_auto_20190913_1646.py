# Generated by Django 2.2.3 on 2019-09-13 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190912_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('Employeer', 'Employeer'), ('Job Seeker', 'Job Seeker')], default='Job Seeker', max_length=15),
        ),
    ]
