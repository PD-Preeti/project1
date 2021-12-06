from django.db import models
from django.utils import timezone

def IST_datetime():
    return timezone.now() + timezone.timedelta(hours=5.5)

class Progress(models.Model):
    person_name = models.CharField(max_length=500, null=True, blank=True)
    person_team = models.CharField(max_length=500, null=True, blank=True)
    person_email = models.EmailField(null=True, blank=True)
    person_location = models.CharField(max_length=50, null=True, blank=True)
    person_firstlevel = models.CharField(max_length=500, null=True, blank=True)
    person_secondlevel = models.CharField(max_length=500, null=True, blank=True)
    person_empid = models.CharField(max_length=50, null=True, blank=True)
    course_name = models.CharField(max_length=500, null=True, blank=True)
    total_modules = models.IntegerField(default=0, null=True, blank=True)
    module_completed = models.IntegerField(default=0, null=True, blank=True)
    progress = models.IntegerField(default=0, null=True, blank=True)
    score = models.IntegerField(default=0, null=True, blank=True)
    testgiven_status = models.BooleanField(default=False)
    couse_assigndate = models.DateTimeField(default=IST_datetime, null=True, blank=True)
    course_completedtime = models.DateTimeField(default=IST_datetime, null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    course_status = models.CharField(default='active', max_length=200, null=True, blank=True)
    test_startflag = models.BooleanField(default=False)
    rating_flag = models.BooleanField(default=False, null=True)
    rating_of_course = models.IntegerField(default=0, blank=True)
    improvement_rem = models.TextField(default=None, null=True, blank=True)


    def __str__(self):
        return  '%s %s' %(self.person_email, self.course_name)

class CompletedModuledetail(models.Model):
    person_email = models.EmailField(default=None, null=True, blank=True)
    person_team = models.CharField(max_length=500, null=True, blank=True)
    course_name = models.CharField(max_length=500, null=True, blank=True)
    completed_module = models.CharField(max_length=500, null=True, blank=True)
    module_completedtime = models.DateTimeField(default=IST_datetime, null=True, blank=True)
    module_status = models.CharField(max_length=500, null=True, blank=True)
    module_confidence = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.person_email

class QuestionAttempted(models.Model):
    person_email = models.EmailField(default=None, blank=True)
    course_name = models.CharField(max_length=500, null=True, blank=True)
    quest_id = models.IntegerField(default=0, blank=True)
    option_given = models.TextField(default=None, null=True)
    is_correct = models.CharField(max_length=100, null=True, blank=True)
    answer_giventime = models.DateTimeField(default=IST_datetime, null=True, blank=True)

    def __str__(self):
        return '%s %s' %(self.person_email, self.course_name)

class PostScenario(models.Model):
    scinario_id = models.IntegerField(default=0, null=True, blank=True)
    person_email = models.EmailField(default=None, null=True, blank=True)
    scinario_answer = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(null=True, blank=True)
    associated_course = models.CharField(max_length=500, null=True, blank=True)
    associated_module = models.CharField(max_length=500, null=True, blank=True)
    submit_time = models.DateTimeField(default=IST_datetime, null=True, blank=True)

class Recommendation(models.Model):
    person_email = models.EmailField(default=None, blank=True)
    user_name = models.CharField(max_length=500, null=True, blank=True)
    user_designation = models.CharField(max_length=500, null=True, blank=True)
    recommended_course = models.CharField(max_length=500, null=True, blank=True)
    recommended_to = models.EmailField(default=None, blank=True)
    recommended_to_name = models.CharField(max_length=500, null=True, blank=True)
    recommended_to_designation = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=100, blank=True, default='NoAction')
    test_flag = models.BooleanField(null=True, blank=True)
    module_count = models.IntegerField(default=0, null=True, blank=True)
    submit_time = models.DateTimeField(default=IST_datetime, null=True, blank=True)

    def __str__(self):
        return "%s %s %s" %(self.person_email, self.recommended_course, self.recommended_to)

class ReportIssue(models.Model):
    person_email = models.EmailField(default=None, blank=True)
    report_title = models.CharField(max_length=500, null=True, blank=True)
    report_description = models.TextField(default=None, null=True, blank=True)
    report_file = models.FileField(upload_to='', null=True, blank=True)
    submit_time = models.DateTimeField(default=IST_datetime, null=True, blank=True)

    def __str__(self):
        return self.report_title

class Contribution(models.Model):
    contributor_email = models.EmailField(default=None, blank=True, null=True)
    contributor_name = models.CharField(max_length=500, null=True, blank=True)
    contributor_team = models.CharField(max_length=500, null=True, blank=True)
    submission_date = models.DateTimeField(default=IST_datetime, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    process_name = models.CharField(max_length=3000, null=True, blank=True)
    case_study = models.FileField(upload_to='', null=True, blank=True)
    supporting_docs = models.FileField(upload_to='', null=True, blank=True)
    status = models.CharField(default='Pending', choices=(('Pending','Pending'),('Accepted','Accepted'),('Rejected','Rejected')), max_length=100, null=True, blank=True)
    remark = models.TextField(default=None, null=True, blank=True)
    score = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.title

class QnA(models.Model):
    progress = models.ForeignKey(Progress, on_delete=models.CASCADE)
    module_name = models.CharField(max_length=200 ,blank=True)
    question = models.TextField(blank=True)
    answer = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Pending', choices=(('Pending','Pending'),('Accepted','Accepted'),('Rejected','Rejected')))
    rejected_remark = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=IST_datetime, blank=True)
    closed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s %s' %(self.progress.person_email, self.progress.course_name)