# Generated by Django 2.2.6 on 2020-07-03 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminboard', '0005_auto_20200703_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='flag',
            field=models.CharField(blank=True, default='Active', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='scenario',
            name='flag',
            field=models.CharField(blank=True, default='Active', max_length=100, null=True),
        ),
    ]