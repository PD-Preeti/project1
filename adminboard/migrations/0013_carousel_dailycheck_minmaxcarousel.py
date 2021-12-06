# Generated by Django 2.2.6 on 2021-01-22 14:45

import adminboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminboard', '0012_auto_20201116_1727'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carousel_type', models.CharField(blank=True, choices=[('Course', 'Course'), ('Other', 'Other')], default='Course', max_length=100, null=True)),
                ('carousel_title', models.CharField(blank=True, max_length=500, null=True)),
                ('carousel_description', models.TextField(blank=True, default=None, null=True)),
                ('carousel_course', models.CharField(blank=True, max_length=500, null=True)),
                ('carousel_link', models.CharField(blank=True, max_length=500, null=True)),
                ('carousel_cover', models.FileField(blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='DailyCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_today', models.DateTimeField(default=adminboard.models.IST_datetime)),
            ],
        ),
        migrations.CreateModel(
            name='MinMaxCarousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min', models.IntegerField(default=0)),
                ('max', models.IntegerField(default=0)),
            ],
        ),
    ]