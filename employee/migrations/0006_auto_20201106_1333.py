# Generated by Django 2.2.6 on 2020-11-06 13:33

from django.db import migrations, models
import employee.models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_progress_rating_flag'),
    ]

    operations = [
        migrations.CreateModel(
            name='RaiseTechIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_email', models.EmailField(blank=True, default=None, max_length=254)),
                ('related_course', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(blank=True, default='NoAction', max_length=100)),
                ('resolved_flag', models.BooleanField(blank=True, default=False, null=True)),
                ('submit_time', models.DateTimeField(blank=True, default=employee.models.IST_datetime, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_email', models.EmailField(blank=True, default=None, max_length=254)),
                ('user_name', models.CharField(blank=True, max_length=500, null=True)),
                ('user_designation', models.CharField(blank=True, max_length=500, null=True)),
                ('recommended_course', models.CharField(blank=True, max_length=500, null=True)),
                ('recommended_to', models.EmailField(blank=True, default=None, max_length=254)),
                ('recommended_to_name', models.CharField(blank=True, max_length=500, null=True)),
                ('recommended_to_designation', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(blank=True, default='NoAction', max_length=100)),
                ('test_flag', models.BooleanField(blank=True, null=True)),
                ('module_count', models.IntegerField(blank=True, default=0, null=True)),
                ('submit_time', models.DateTimeField(blank=True, default=employee.models.IST_datetime, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='completedmoduledetail',
            name='module_completedtime',
            field=models.DateTimeField(blank=True, default=employee.models.IST_datetime, null=True),
        ),
        migrations.AlterField(
            model_name='postscenario',
            name='submit_time',
            field=models.DateTimeField(blank=True, default=employee.models.IST_datetime, null=True),
        ),
        migrations.AlterField(
            model_name='progress',
            name='course_completedtime',
            field=models.DateTimeField(blank=True, default=employee.models.IST_datetime, null=True),
        ),
        migrations.AlterField(
            model_name='progress',
            name='couse_assigndate',
            field=models.DateTimeField(blank=True, default=employee.models.IST_datetime, null=True),
        ),
        migrations.AlterField(
            model_name='questionattempted',
            name='answer_giventime',
            field=models.DateTimeField(blank=True, default=employee.models.IST_datetime, null=True),
        ),
    ]
