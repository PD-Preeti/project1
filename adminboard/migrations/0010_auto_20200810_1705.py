# Generated by Django 2.2.6 on 2020-08-10 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminboard', '0009_auto_20200729_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='file1',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='module',
            name='file2',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]