# Generated by Django 2.2.3 on 2019-09-15 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_auto_20190913_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='product',
            field=models.IntegerField(null=True),
        ),
    ]
