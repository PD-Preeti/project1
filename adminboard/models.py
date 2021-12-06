from django.db import models
from django.utils import timezone

def IST_datetime():
    return timezone.now() + timezone.timedelta(hours=5.5)

class AuthorizedPanel(models.Model):
    admin_name = models.CharField(max_length=500, null=True, blank=True)
    admin_email = models.EmailField(null=True, blank=True)
    admin_addedtime = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.admin_name

class Module(models.Model):
    module_name = models.CharField(max_length=500, null=True, blank=True, unique=True)
    module_number = models.IntegerField(null=True, blank=True, default=0)
    file1 = models.FileField(upload_to='', null=True, blank=True)
    file2 = models.FileField(upload_to='', null=True, blank=True)
    file3 = models.FileField(upload_to='', null=True, blank=True)
    file4 = models.FileField(upload_to='', null=True, blank=True)
    file5 = models.FileField(upload_to='', null=True, blank=True)
    file6 = models.FileField(upload_to='', null=True, blank=True)
    file7 = models.FileField(upload_to='', null=True, blank=True)
    file8 = models.FileField(upload_to='', null=True, blank=True)
    file9 = models.FileField(upload_to='', null=True, blank=True)
    file10 = models.FileField(upload_to='', null=True, blank=True)
    file11 = models.FileField(upload_to='', null=True, blank=True)
    file12 = models.FileField(upload_to='', null=True, blank=True)
    file13 = models.FileField(upload_to='', null=True, blank=True)
    file14 = models.FileField(upload_to='', null=True, blank=True)
    process_name = models.CharField(max_length=1000, null=True, blank=True)
    location = models.CharField(max_length=1000, null=True, blank=True)
    module_addedtime = models.DateTimeField(default=IST_datetime, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True, default='Active')
    video_file = models.FileField(upload_to='', null=True, blank=True)
    link1 = models.CharField(max_length=1000, null=True, blank=True,)
    link2 = models.CharField(max_length=1000, null=True, blank=True,)
    link3 = models.CharField(max_length=1000, null=True, blank=True,)
    link4 = models.CharField(max_length=1000, null=True, blank=True,)
    link5 = models.CharField(max_length=1000, null=True, blank=True,)
    link6 = models.CharField(max_length=1000, null=True, blank=True,)
    link7 = models.CharField(max_length=1000, null=True, blank=True,)
    link8 = models.CharField(max_length=1000, null=True, blank=True,)
    link9 = models.CharField(max_length=1000, null=True, blank=True,)
    link10 = models.CharField(max_length=1000, null=True, blank=True,)


    def __str__(self):
        return self.module_name

class Course(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True)
    id_of_module = models.IntegerField(null=True, blank=True)
    sequence_num = models.IntegerField(null=True, blank=True)
    course_name = models.CharField(max_length=500, null=True, blank=True)
    course_team = models.CharField(max_length=500, null=True, blank=True)
    course_createdtime = models.DateTimeField(default=IST_datetime, null=True, blank=True)
    course_status = models.CharField(max_length=200, null=True, blank=True, default=None)
    test_time = models.IntegerField(default=30, null=True, blank=True)
    course_cover = models.FileField(upload_to='', blank=True)
    final_questcount = models.IntegerField(default=20, null=True)
    created_time = models.DateTimeField(default=IST_datetime, null=True, blank=True)
    updated_time = models.DateTimeField(default=IST_datetime, null=True, blank=True)



    def __str__(self):
        return self.course_name

class Scenario(models.Model):
    scenario_desc = models.TextField(default=None, null=True, blank=True)
    option1 = models.TextField(default=None, null=True, blank=True)
    option2 = models.TextField(default=None, null=True, blank=True)
    option3 = models.TextField(default=None, null=True, blank=True)
    option4 = models.TextField(default=None, null=True, blank=True)
    correctoption = models.TextField(default=None, null=True, blank=True)
    associated_module = models.CharField(max_length=500, null=True, blank=True)
    reason = models.TextField(default=None, blank=True, null=True)
    scenario_file = models.FileField(upload_to='', null=True, blank=True)
    scenario_addedtime = models.DateTimeField(default=IST_datetime, null=True, blank=True)
    flag = models.CharField(max_length=100, default='Active', null=True, blank=True)


    def __str__(self):
        return self.scenario_desc

class Question(models.Model):
    module_name = models.CharField(max_length=500, null=True, blank=True)
    question = models.TextField(default=None, null=True, blank=True)
    option1 = models.TextField(default=None, null=True, blank=True)
    option2 = models.TextField(default=None, null=True, blank=True)
    option3 = models.TextField(default=None, null=True, blank=True)
    option4 = models.TextField(default=None, null=True, blank=True)
    correct_option = models.TextField(default=None, null=True, blank=True)
    quest_file = models.FileField(upload_to='', null=True, blank=True)
    flag = models.CharField(max_length=100, default='Active', null=True, blank=True)


    def __str__(self):
        return '%s %s' %(self.module_name, self.question)

class Process(models.Model):
    process_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.process_name

class Carousel(models.Model):
    carousel_type = models.CharField(default='Course', choices=(('Course','Course'),('Other','Other')), max_length=100, null=True, blank=True)
    carousel_title = models.CharField(max_length=500, null=True, blank=True)
    carousel_description = models.TextField(default=None, null=True, blank=True)
    carousel_course = models.CharField(max_length=500, null=True, blank=True)
    carousel_link = models.CharField(max_length=500, null=True, blank=True)
    carousel_cover = models.FileField(upload_to='', blank=True)

    def __str__(self):
        return self.carousel_title

class MinMaxCarousel(models.Model):
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=0)


class DailyCheck(models.Model):
    date_today = models.DateTimeField(default=IST_datetime)