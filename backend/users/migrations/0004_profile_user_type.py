# Generated by Django 2.2.3 on 2019-07-30 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[(1, 'seeker'), (2, 'giver')], default='', max_length=15),
            preserve_default=False,
        ),
    ]
