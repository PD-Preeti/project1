# Generated by Django 2.2.6 on 2020-07-03 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminboard', '0004_auto_20200703_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='location',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
