# Generated by Django 2.1.1 on 2019-11-11 04:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import room.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to=room.models.get_image_filename, verbose_name='Image')),
            ],
        ),
        migrations.CreateModel(
            name='PostedRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner_name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('conditon', models.TextField(blank=True, null=True)),
                ('price', models.IntegerField()),
                ('contact', models.CharField(max_length=15)),
                ('facility', models.ManyToManyField(to='room.Facility')),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kitchen', models.IntegerField()),
                ('bedroom', models.IntegerField()),
                ('hall', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='roomtype',
            unique_together={('kitchen', 'bedroom', 'hall')},
        ),
        migrations.AddField(
            model_name='postedroom',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room.RoomType'),
        ),
        migrations.AddField(
            model_name='postedroom',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='image',
            name='posted_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room.PostedRoom'),
        ),
        migrations.AddField(
            model_name='facility',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room.RoomType'),
        ),
        migrations.AlterUniqueTogether(
            name='facility',
            unique_together={('room_type', 'title')},
        ),
    ]