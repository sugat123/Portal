# Generated by Django 2.2.3 on 2019-09-15 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_auto_20190915_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.IntegerField(null=True),
        ),
    ]