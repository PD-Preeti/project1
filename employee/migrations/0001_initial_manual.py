# Generated by Django 2.2.6 on 2020-03-18 12:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompletedModuledetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('person_team', models.CharField(blank=True, max_length=500, null=True)),
                ('course_name', models.CharField(blank=True, max_length=500, null=True)),
                ('completed_module', models.CharField(blank=True, max_length=500, null=True)),
                ('module_completedtime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('module_status', models.CharField(blank=True, max_length=500, null=True)),
                ('module_confidence', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostScenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scinario_id', models.IntegerField(blank=True, default=0, null=True)),
                ('person_email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('scinario_answer', models.TextField(blank=True, null=True)),
                ('is_correct', models.BooleanField(blank=True, null=True)),
                ('associated_course', models.CharField(blank=True, max_length=500, null=True)),
                ('associated_module', models.CharField(blank=True, max_length=500, null=True)),
                ('submit_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.CharField(blank=True, max_length=500, null=True)),
                ('person_team', models.CharField(blank=True, max_length=500, null=True)),
                ('person_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('person_location', models.CharField(blank=True, max_length=50, null=True)),
                ('person_firstlevel', models.CharField(blank=True, max_length=500, null=True)),
                ('person_secondlevel', models.CharField(blank=True, max_length=500, null=True)),
                ('person_empid', models.CharField(blank=True, max_length=50, null=True)),
                ('course_name', models.CharField(blank=True, max_length=500, null=True)),
                ('total_modules', models.IntegerField(blank=True, default=0, null=True)),
                ('module_completed', models.IntegerField(blank=True, default=0, null=True)),
                ('progress', models.IntegerField(blank=True, default=0, null=True)),
                ('score', models.IntegerField(blank=True, default=0, null=True)),
                ('testgiven_status', models.BooleanField(default=False)),
                ('couse_assigndate', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('course_completedtime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('expiration_date', models.DateTimeField(blank=True, null=True)),
                ('course_status', models.CharField(blank=True, default='active', max_length=200, null=True)),
                ('test_startflag', models.BooleanField(default=False)),
                ('rating_of_course', models.IntegerField(blank=True, default=0)),
                ('improvement_rem', models.TextField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAttempted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_email', models.EmailField(blank=True, default=None, max_length=254)),
                ('course_name', models.CharField(blank=True, max_length=500, null=True)),
                ('quest_id', models.IntegerField(blank=True, default=0)),
                ('option_given', models.TextField(blank=True, default=None)),
                ('is_correct', models.CharField(blank=True, max_length=100, null=True)),
                ('answer_giventime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
    ]