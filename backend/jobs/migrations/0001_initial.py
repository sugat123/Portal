# Generated by Django 2.2.3 on 2019-10-23 04:20

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.ImageField(default='default.jpg', upload_to='banner')),
                ('login_register', models.ImageField(default='default.jpg', upload_to='banner')),
                ('dashboard', models.ImageField(default='default.jpg', upload_to='banner')),
                ('newsfeed', models.ImageField(default='default.jpg', upload_to='banner')),
                ('newsfeed_detail', models.ImageField(default='default.jpg', upload_to='banner')),
                ('job', models.ImageField(default='default.jpg', upload_to='banner')),
                ('app', models.ImageField(default='default.jpg', upload_to='banner')),
                ('app_bg', models.ImageField(default='default.jpg', upload_to='banner')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('match_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Facility',
            },
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='jobtypes')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique_with=('id',))),
                ('commission', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Job Types',
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_id', models.IntegerField()),
                ('applied_id', models.IntegerField()),
                ('score', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('job_type', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Matched Jobs',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_id', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('amount', models.IntegerField(null=True)),
                ('product', models.IntegerField(null=True)),
                ('mobile', models.CharField(max_length=20, null=True)),
                ('created_on', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Payments',
            },
        ),
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='setting')),
                ('about_text', models.TextField()),
                ('address', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('website', models.URLField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.IntegerField()),
                ('user_id', models.IntegerField(null=True)),
                ('paid_status', models.BooleanField(default=False, null=True)),
                ('match_id', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Verified Payments',
            },
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('job_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.JobType')),
            ],
            options={
                'unique_together': {('job_type', 'title')},
            },
        ),
        migrations.CreateModel(
            name='PostedJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.IntegerField(blank=True, null=True)),
                ('salary', models.IntegerField(blank=True, null=True)),
                ('working_time', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('number_of_employee', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='user', unique_with=('id',))),
                ('facility', models.ManyToManyField(blank=True, to='jobs.Facility')),
                ('job_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.JobType')),
                ('skills', models.ManyToManyField(blank=True, to='jobs.Skills')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Posted Jobs',
            },
        ),
        migrations.AddField(
            model_name='facility',
            name='job_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.JobType'),
        ),
        migrations.CreateModel(
            name='AppliedJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.IntegerField(blank=True, null=True)),
                ('location', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='user', unique_with=('id',))),
                ('job_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.JobType')),
                ('skills', models.ManyToManyField(blank=True, to='jobs.Skills')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Applied Jobs',
            },
        ),
        migrations.AlterUniqueTogether(
            name='facility',
            unique_together={('job_type', 'title')},
        ),
    ]
