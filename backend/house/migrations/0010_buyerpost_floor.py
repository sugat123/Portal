# Generated by Django 2.1.1 on 2019-11-14 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0009_buyerpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyerpost',
            name='floor',
            field=models.IntegerField(null=True),
        ),
    ]