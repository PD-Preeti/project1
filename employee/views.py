from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from employee.models import Progress, CompletedModuledetail, QuestionAttempted, PostScenario, Recommendation, ReportIssue, Contribution, QnA
from adminboard.models import Course, Scenario, Question, Process, MinMaxCarousel, Carousel
import math
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta, date
from sqlalchemy import create_engine
import socket
import pandas as pd
from django.db.models import Avg, Q, Count
from django.core.mail import send_mail
from django.contrib import messages
from django.core.paginator import Paginator
import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from adminboard.mails import WelcomeMail


SENDER = 'analytics@dataflowgroup.com'
USERNAME_SMTP = "AKIA6MOGWBGBCBL3LFR3"
PASSWORD_SMTP = "BBighTezVs/o++KjQFieuL7sJO+Xe9CmAk96KhcC2eyv"
HOST = "email-smtp.eu-west-1.amazonaws.com"
PORT = 587

def authentication_check(user):
    return user.is_authenticated

def employeelogin(request):
    settings.LOGIN_REDIRECT_URL = '/home/'
    return render(request, 'employee/login.html')

def cleanse_data():
    # cleanse data
    if Progress.objects.filter(person_name__icontains='employee').exists():
        for i in Progress.objects.filter(person_name__icontains='employee'):
            list_name = (i.person_name).split()
            name_list = []
            for name in list_name[2:]:
                if name != 'Employee':
                    name_list.append(name)
                else:
                    break
            name_of_employee = ' '.join(name_list)
            i.person_name = name_of_employee
            i.save()
        return True
    else:
        return False



@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def employeehome(request):
    # cleanse data
    is_cleansed = cleanse_data()

    entry_email = request.user.email
    first_name = request.user.first_name
    my_detail = Progress.objects.filter(person_email__iexact=entry_email).exclude(course_status__iexact='deleted')
    courses = [(i.course_name, i.progress, i.testgiven_status, i.score, i.expiration_date, i.course_status, i.rating_of_course) for i in my_detail]
    course_cover = Course.objects.values('course_name').distinct()
    minmax = MinMaxCarousel.objects.all().last()
    carousels = Carousel.objects.all()
    for i in course_cover:
        cover = Course.objects.filter(course_name__iexact=i['course_name'])[0].course_cover
        i['course_cover'] = cover
    # pending courses
    pending_courses = [(i.course_name, i.progress, i.testgiven_status, i.score, i.expiration_date, i.course_status) for i in Progress.objects.filter(person_email__iexact=entry_email, testgiven_status__exact=False).exclude(course_status__iexact='deleted')]
    completed_courses = [(i.course_name, i.progress, i.testgiven_status, i.score, i.expiration_date, i.course_status, i.rating_of_course) for i in Progress.objects.filter(person_email__iexact=entry_email, testgiven_status__exact=True)]
    #low confidence modules and incorrect scenario and courses
    low_conf_mod = CompletedModuledetail.objects.filter(person_email__iexact=entry_email, module_confidence__iexact='Low', module_status__iexact='Active')
    incorrect_scenarios = PostScenario.objects.filter(person_email__iexact=entry_email, is_correct=False, submit_time__month=datetime.now().month)
    sc_data = []
    for i in incorrect_scenarios:
        sc_obj = Scenario.objects.get(pk=i.scinario_id)
        sc_data.append((sc_obj.associated_module, i.associated_course))
    sc_data_set = set(sc_data)
    sc_data = list(sc_data_set)


    # check questions
    courses_assgined = [i.course_name for i in Progress.objects.filter(person_email__iexact=entry_email).exclude(course_status__iexact='deleted')]
    course_and_quest = []
    for i in courses_assgined:
        modules_in_c = [j.module.module_name for j in Course.objects.filter(course_name__iexact=i)]
        quest_count = Question.objects.filter(module_name__in=modules_in_c).count()
        course_and_quest.append((i, quest_count))

    # test flag update
    course_with_0 = [i[0] for i in course_and_quest if i[1] == 0]
    Progress.objects.filter(person_email__iexact=entry_email, course_name__in=course_with_0).update(testgiven_status=True)
    
    # new project view
    new_proj_all_courses = Course.objects.order_by().values('course_name', 'course_cover', 'course_status', 'course_team', 'test_time', 'created_time').distinct()
    new_proj_all_courses2 = []
    course_names = []
    for i in list(new_proj_all_courses):
        if i['course_name'] not in course_names:
            course_names.append(i['course_name'])
            badgetime = i['created_time'] + timedelta(days = 7)
            badgetime = datetime.strptime(str(badgetime)[:19], "%Y-%m-%d %H:%M:%S")
            todays_date = datetime.strptime(str(datetime.now())[:19], "%Y-%m-%d %H:%M:%S")
            if todays_date < badgetime:
                badge = True
            else:
                badge = False
            new_proj_all_courses2.append((i['course_name'], i['course_cover'], i['course_status'], i['course_team'], i['test_time'], badge))

    # recommendations
    recommendation_count = Recommendation.objects.filter(recommended_to__iexact=entry_email, status__iexact='NoAction').count()
    date_today = (timezone.now() + timezone.timedelta(hours=5.5)).date()
    
    # avg rating course wise
    all_assingned_avg_rating = list(Progress.objects.filter(rating_flag=True).values('course_name').annotate(avg_rating=Avg('rating_of_course')))

    courses_not_assigned = list(set([i.course_name for i in Course.objects.all() if i.course_name not in [j['course_name'] for j in all_assingned_avg_rating]]))

    for j in courses_not_assigned:
        to_append = {}
        to_append['course_name'] = j
        to_append['avg_rating'] = 0
        all_assingned_avg_rating.append(to_append)
    for i in all_assingned_avg_rating:
        people_count = Progress.objects.filter(course_name__iexact=i['course_name'], course_status__iexact='active').count()
        module_count = Course.objects.filter(course_name__iexact=i['course_name'], course_status__iexact='Active').count()
        i['people_count'] = people_count
        i['module_count'] = module_count

        
    
    return render(request, 'employee/home.html', {'recommendation_count': recommendation_count, 'courses': courses, 'date_today': date_today, 'pending_course_count': len(pending_courses), 'pending_courses': pending_courses, 'completed_courses': completed_courses, 'low_conf_mod': low_conf_mod, 'sc_data': sc_data, 'first_name': first_name, 'course_cover': course_cover, 'new_proj_all_courses2': new_proj_all_courses2, 'all_assingned_avg_rating': all_assingned_avg_rating, 'minmax': minmax, 'carousels': carousels})

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def logout_emp(request):
    logout(request)
    return redirect('employee:employeelogin')

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def your_courses(request):
    first_name = request.user.first_name
    entry_email = request.user.email
    my_detail = Progress.objects.filter(person_email__iexact=entry_email).exclude(course_status__iexact='deleted')
    courses = [(i.course_name, i.progress, i.testgiven_status, i.score, i.expiration_date, i.course_status, i.rating_of_course, i.couse_assigndate) for i in my_detail]
    course_cover = Course.objects.values('course_name').distinct()
    for i in course_cover:
        cover = Course.objects.filter(course_name__iexact=i['course_name'])[0].course_cover
        mods = Course.objects.filter(course_name__iexact=i['course_name'])
        # Updated Badge
        updated_time = datetime.strptime(str(Course.objects.filter(course_name__iexact=i['course_name'])[0].updated_time)[:19], "%Y-%m-%d %H:%M:%S")
        created_time = datetime.strptime(str(Course.objects.filter(course_name__iexact=i['course_name'])[0].created_time)[:19], "%Y-%m-%d %H:%M:%S")

        todays_date = datetime.today() + timedelta(hours=5.5)

        if created_time == updated_time:
            badge = False
        else:
            todays_date = todays_date.strftime('%Y/%m/%d').split('/')
            updated_time = updated_time.strftime('%Y/%m/%d').split('/')

            todays_date = date(int(todays_date[0]), int(todays_date[1]), int(todays_date[2]))
            updated_time = date(int(updated_time[0]), int(updated_time[1]), int(updated_time[2]))
            delta = updated_time - todays_date
            days = delta.days
            if days < 7:
                badge = True
            else:
                badge = False

        if Course.objects.filter(course_name__iexact=i['course_name'])[0].test_time == 0:
            test_available = 'NA'
        else:
            test_available = 'Yes'
        i['course_cover'] = cover
        i['modules_len'] = len(mods)
        i['test_available'] = test_available
        i['badge'] = badge

    # pending courses
    pending_courses = [(i.course_name, i.progress, i.testgiven_status, i.score, i.expiration_date, i.course_status) for i in Progress.objects.filter(person_email__iexact=entry_email, testgiven_status__exact=False)]
    completed_courses = [(i.course_name, i.progress, i.testgiven_status, i.score, i.expiration_date, i.course_status, i.rating_of_course) for i in Progress.objects.filter(person_email__iexact=entry_email, testgiven_status__exact=True)]

    # check questions
    courses_assgined = [i.course_name for i in Progress.objects.filter(person_email__iexact=entry_email).exclude(course_status__iexact='deleted')]
    course_and_quest = []
    for i in courses_assgined:
        modules_in_c = [j.module.module_name for j in Course.objects.filter(course_name__iexact=i)]
        quest_count = Question.objects.filter(module_name__in=modules_in_c).count()
        course_and_quest.append((i, quest_count))
    # print(course_and_quest)

    # test flag update
    course_with_0 = [i[0] for i in course_and_quest if i[1] == 0]
    Progress.objects.filter(person_email__iexact=entry_email, course_name__in=course_with_0).update(testgiven_status=True)

    # recommendations
    recommendation_count = Recommendation.objects.filter(recommended_to__iexact=entry_email, status__iexact='NoAction').count()
    date_today = (timezone.now() + timezone.timedelta(hours=5.5)).date()
    # updated time
    updated_times = Course.objects.values('course_name', 'updated_time')


    #low confidence modules and incorrect scenario and courses
    low_conf_mod = CompletedModuledetail.objects.filter(person_email__iexact=entry_email, module_confidence__iexact='Low', module_status__iexact='Active')
    incorrect_scenarios = PostScenario.objects.filter(person_email__iexact=entry_email, is_correct=False, submit_time__month=datetime.now().month)
    sc_data = []
    for i in incorrect_scenarios:
        sc_obj = Scenario.objects.get(pk=i.scinario_id)
        sc_data.append((sc_obj.associated_module, i.associated_course))
    sc_data_set = set(sc_data)
    sc_data = list(sc_data_set)
    return render(request, 'employee/your_courses.html', {'recommendation_count': recommendation_count, 'course_and_quest': course_and_quest, 'courses': courses, 'date_today': date_today, 'pending_course_count': len(pending_courses), 'pending_courses': pending_courses, 'updated_times': updated_times, 'low_conf_mod': low_conf_mod, 'sc_data': sc_data,
                                                  'completed_courses': completed_courses, 'first_name': first_name, 'course_cover': course_cover})

@user_passes_test(authentication_check, login_url='/', redirect_field_name='None')
def continuecourse(request, cname):
    global df_all
    employee_entering = str(request.user.email)
    employee_email = employee_entering.lower()
    entry_email = request.user.email.lower()
    first_name = request.user.first_name
    if Progress.objects.filter(person_email=employee_email, course_name=cname).exists():
        enrolled = True
        testgiven_status = Progress.objects.get(person_email=employee_email, course_name=cname).testgiven_status
        score = Progress.objects.get(person_email=employee_email, course_name=cname).score
        course_status = Progress.objects.get(person_email=employee_email, course_name=cname).course_status
        expiration_date = Progress.objects.get(person_email=employee_email, course_name=cname).expiration_date
    else:
        enrolled = False
        score = ''
        testgiven_status = ''
        course_status = ''
        expiration_date = ''
    course = Course.objects.filter(course_name__exact=cname, course_status__iexact='active').order_by('sequence_num')
    modules_in_course = [i.module.module_name for i in course if i.module.status == 'Active']
    completed_modules = [i.completed_module for i in CompletedModuledetail.objects.filter(person_email__exact=employee_email, course_name__iexact=cname, module_status__iexact='Active')]
    scenarios = Scenario.objects.filter(associated_module__in=modules_in_course, flag__iexact='Active')
    
    # get days left before course expires
    date_today = (timezone.now() + timezone.timedelta(hours=5.5)).date()
    if Progress.objects.filter(person_email=employee_email, course_name=cname).exists() and expiration_date != None:
        exp_date = expiration_date.date()
        day_left = exp_date - date_today
        day_left = str(day_left).split(',')[0]
    else:
        day_left = 'Available'
    bool_obj = Progress.objects.filter(person_email__iexact=employee_email, course_name__iexact=cname).exists()
    if modules_in_course and bool_obj:
        #course cover
        course_cover = Course.objects.filter(course_name__iexact=cname)[0].course_cover
        # check questions
        courses_assgined = [i.course_name for i in Progress.objects.filter(person_email__iexact=entry_email).exclude(course_status__iexact='deleted')]
        progress = True
        course_and_quest = []
        for i in courses_assgined:
            modules_in_c = [j.module.module_name for j in Course.objects.filter(course_name__iexact=i)]
            quest_count = Question.objects.filter(module_name__in=modules_in_c).count()
            if Course.objects.filter(course_name__iexact=i).exists():
                if Course.objects.filter(course_name__iexact=i)[0].test_time == 0:
                    test_available = 'NA'
                else:
                    test_available = 'Yes'

                updated_time = Course.objects.filter(course_name__iexact=cname)[0].updated_time
            else:
                test_available = ''
                updated_time = ''

            course_and_quest.append((i, quest_count, updated_time, test_available))
    else:
        # course cover
        progress = False
        course_cover = Course.objects.filter(course_name__iexact=cname)[0].course_cover
        course_and_quest = []
        modules_in_c = [j.module.module_name for j in Course.objects.filter(course_name__iexact=cname)]
        quest_count = Question.objects.filter(module_name__in=modules_in_c).count()
        quest_in_c = Course.objects.filter(course_name__iexact=cname)[0].final_questcount
        course_test_time = Course.objects.filter(course_name__iexact=cname)[0].test_time
        updated_time = Course.objects.filter(course_name__iexact=cname)[0].updated_time
        course_and_quest.append((cname, quest_count, updated_time, quest_in_c, course_test_time))


    # Course Review Details
    comments_in_c = Progress.objects.filter(course_name__iexact=cname).exclude(improvement_rem='').exclude(improvement_rem=None).order_by('-course_completedtime').values('person_name', 'person_email', 'person_team', 'improvement_rem', 'rating_of_course', 'course_completedtime')
    paginator = Paginator(comments_in_c, 6) # change here
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # on server
    if socket.gethostbyname(socket.gethostname()) == '10.2.5.128' or socket.gethostbyname(socket.gethostname()) == '10.2.1.230':
        engine = create_engine('postgresql://analytics:analytics@123@ec2-34-246-108-106.eu-west-1.compute.amazonaws.com:5432/iadatabase')
        df_aws = pd.read_sql_query('select * from "headcount_master_darwinbox"', con=engine)
        df = df_aws[['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting', 'Employee Code', '1st Level Reporting Email ID', 'Function Head Email ID', 'Designation']]
        df['Email Id'] = df['Email Id'].str.lower()

        try:
            teams = set([i for i in df['Sub-Department']])
            user_designation = df[df['Email Id']==employee_email]['Designation'].values[0]
            user_name = df[df['Email Id']==employee_email]['Employee Name'].values[0]
            not_a_user = False
        except:
            teams = ''
            user_designation = ''
            user_name = ''
            not_a_user = True

        df_designation = df[['Email Id', 'Designation']]
        df_designation_tuple = [tuple(x) for x in df_designation.values]
        df = df.loc[(df['1st Level Reporting Email ID'] == entry_email) | (df['Function Head Email ID'] == entry_email), :]
        if len(df):
            df['Enrolled'] = df.apply(lambda x: True if Progress.objects.filter(person_email=x['Email Id'], course_name=cname, course_status='active').exists() else False, axis=1)
            df['Recommended'] = df.apply(lambda x: True if Recommendation.objects.filter(recommended_to=x['Email Id'], recommended_course=cname).filter(Q(status__iexact='NoAction') | Q(status__iexact='Accepted')).exists() else False, axis=1)

            employee_detail_dict = [tuple(x) for x in df[['Employee Name', 'Email Id', 'Enrolled', 'Recommended', 'Designation']].to_numpy()]
        else:
            employee_detail_dict = []
            

    # on development
    else:
        df = pd.DataFrame(columns=['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting',
                                    '2nd Level Reporting', 'Employee Code', '1st Level Reporting Email ID', 'Function Head Email ID', 'Designation'])
        df.loc[0] = ['Ankur singh', 'ankurkalakoti@gmail.com', 'Analytcs', 'Noida', 'Rathore', 'agarwal', '11111', 'officialankursingh97@gmail.com', 'agarwal@mail.com', 'Associate II']
        df.loc[1] = ['Anubhav kumar', 'anubhav.kumar27@gmail.com', 'Analytcs', 'Noida', 'Rathore', 'agarwal', '11111', 'officialankursingh97@gmail.com', 'princeroyale72@gmail.com', 'Associate I']
        df.loc[2] = ['OFFANKUR 2', 'princeroyale72@gmail.com', 'Analytcs', 'Noida', 'Rathore', 'agarwal', '11111', 'anubhav.kumar27@gmail.com', 'agarwal@mail.com', 'Associate I']
        df['Email Id'] = df['Email Id'].str.lower()
        try:
            teams = set([i for i in df['Sub-Department']])
            user_designation=df[df['Email Id']==employee_email]['Designation'].values[0]
            user_name=df[df['Email Id']==employee_email]['Employee Name'].values[0]
            not_a_user = False
        except:
            teams = ''
            user_designation = ''
            user_name = ''
            not_a_user = True

        df_designation = df[['Email Id', 'Designation']]
        df_designation_tuple = [tuple(x) for x in df_designation.values]
        df = df.loc[(df['1st Level Reporting Email ID'] == entry_email) | (df['Function Head Email ID'] == entry_email), :]
        if len(df):
            df['Enrolled'] = df.apply(lambda x: True if Progress.objects.filter(person_email=x['Email Id'], course_name=cname, course_status='active').exists() else False, axis=1)
            df['Recommended'] = df.apply(lambda x: True if Recommendation.objects.filter(recommended_to=x['Email Id'], recommended_course=cname).filter(Q(status__iexact='NoAction') | Q(status__iexact='Accepted')).exists() else False, axis=1)

            employee_detail_dict = [tuple(x) for x in df[['Employee Name', 'Email Id', 'Enrolled', 'Recommended', 'Designation']].to_numpy()]
        else:
            employee_detail_dict = []

    # recommendation_count
    recommendation_count = Recommendation.objects.filter(recommended_to__iexact=entry_email, status__iexact='NoAction').count()
    


    rating_dict = list(Progress.objects.filter(rating_flag=True).values('course_name').annotate(avg_rating=Avg('rating_of_course')))
    if rating_dict:
        for i in rating_dict:
            if i['course_name'] == cname:
                rating = i['avg_rating']
                break
            else:
                rating = 0
    else:
        rating = 0



    people_count = Progress.objects.filter(course_name__iexact=cname, course_status__iexact='active').count()
    
    rating_groups = list(Progress.objects.filter(course_name__iexact=cname, course_status__iexact='active', rating_flag=True).values('rating_of_course').annotate(total=Count('rating_of_course')).order_by('total'))
    total_rating = Progress.objects.filter(course_name__iexact=cname, course_status__iexact='active', rating_flag=True).count()
    for i in rating_groups:
        i['perc'] = (i['total']/total_rating) * 100

    rating_t = []
    if not any(i['rating_of_course'] == 1 for i in rating_groups):
        rating_t.append(0)
    else:
        for pair in rating_groups:
            if pair['rating_of_course'] == 1:
                rating_t.append(pair['perc'])

    if not any(i['rating_of_course'] == 2 for i in rating_groups):
        rating_t.append(0)
    else:
        for pair in rating_groups:
            if pair['rating_of_course'] == 2:
                rating_t.append(pair['perc'])

    if not any(i['rating_of_course'] == 3 for i in rating_groups):
        rating_t.append(0)
    else:
        for pair in rating_groups:
            if pair['rating_of_course'] == 3:
                rating_t.append(pair['perc'])

    if not any(i['rating_of_course'] == 4 for i in rating_groups):
        rating_t.append(0)
    else:
        for pair in rating_groups:
            if pair['rating_of_course'] == 4:
                rating_t.append(pair['perc'])

    if not any(i['rating_of_course'] == 5 for i in rating_groups):
        rating_t.append(0)
    else:
        for pair in rating_groups:
            if pair['rating_of_course'] == 5:
                rating_t.append(pair['perc'])


    return render(request, 'employee/insidecourse.html', {'rating_t': rating_t, 'people_count': people_count, 'rating': rating, 'recommendation_count': recommendation_count,'employee_detail_dict': employee_detail_dict, 'course_and_quest': course_and_quest, 'course': course, 'scenarios': scenarios, 'course_name':cname, 'course_status': course_status, 'expiration_date': expiration_date, 'first_name':first_name, 'enrolled': enrolled, 'user_name': user_name, 'user_designation': user_designation, 'progress':progress, 'comments_in_c': comments_in_c,
                                                          'date_today': date_today, 'day_left': day_left, 'course_cover': course_cover, 'course_and_quest':course_and_quest, 'modules_in_course':modules_in_course,
                                                          'total_mod_count': len(course), 'completed_mod_count': len(completed_modules), 'score': score, 'not_a_user': not_a_user, 'page_obj': page_obj, 'df_designation_tuple': df_designation_tuple})

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def coursestarted(request, cname):
    email = request.user.email
    entry_email = request.user.email
    first_name = request.user.first_name
    testgiven_status = Progress.objects.get(person_email=str(entry_email).lower(), course_name=cname).testgiven_status
    teststart_status = Progress.objects.get(person_email=str(entry_email).lower(), course_name=cname).test_startflag
    course = Course.objects.filter(course_name__exact=cname).order_by('sequence_num')

    modules_in_course = [i.module.module_name for i in course]
    scenarios = Scenario.objects.filter(associated_module__in=modules_in_course, flag__iexact='Active')
    # check for completed modules
    completed_modules = [(i.completed_module, i.module_confidence) for i in CompletedModuledetail.objects.filter(person_email__exact=email, course_name__iexact=cname, module_status__iexact='Active')]
    total_modules = len(course)
    progress = math.ceil(len(set(completed_modules))/total_modules * 100)
    Progress.objects.filter(person_email__exact=email, course_name__iexact=cname).update(progress=progress, total_modules=total_modules, module_completed=len(completed_modules))
    #course status
    course_status = Progress.objects.get(person_email=str(email).lower(), course_name=cname).course_status
    expiration_date = Progress.objects.get(person_email=str(email).lower(), course_name=cname).expiration_date

    # check questions
    courses_assgined = [i.course_name for i in Progress.objects.filter(person_email__iexact=entry_email).exclude(course_status__iexact='deleted')]
    course_and_quest = []
    for i in courses_assgined:
        modules_in_c = [j.module.module_name for j in Course.objects.filter(course_name__iexact=i)]
        quest_count = Question.objects.filter(module_name__in=modules_in_c).count()
        course_and_quest.append((i, quest_count))

    # rating flag
    rating_flag = Progress.objects.get(person_email__exact=str(entry_email).lower(), course_name__iexact=cname).rating_flag

    # recommendation_count
    recommendation_count = Recommendation.objects.filter(recommended_to__iexact=entry_email, status__iexact='NoAction').count()
    date_today = (timezone.now() + timezone.timedelta(hours=5.5)).date()

    # all scenarios
    scenarios_all = PostScenario.objects.filter(associated_course__iexact=cname,
    person_email__iexact=entry_email)

    # QnA
    quest_answer = QnA.objects.filter(progress__course_name__iexact=cname, progress__person_email__iexact=entry_email).order_by('-created_date')
    if request.method == 'POST':
        employee_email = str(request.user.email).lower()
        module_name = request.POST.get('module_name')
        question = request.POST.get('question')
        obj = Progress.objects.get(course_name=cname, person_email=employee_email)
        QnA.objects.create(progress=obj, module_name=module_name, question=question)
                
        # # Mail Formatter

        welcome_mail = WelcomeMail()
        from_email = 'studyhall@dataflowgroup.com'
        subject = f"Query on studyhall"
        title = f"You have query on module: {obj.module_name}"
        content = f"{obj.progress.person_name} have asked a query in module {obj.module_name} today.\n\nClick the button below to reply!\n\nHappy Learning!"
        button_label = "Studyhall Adminboard"
        button_link = f"https://uatcab.dfgateway.com/adminboard/"
        welcome_mail.set_context(subject, title, content, button_label, button_link)
        welcome_mail.send(['ankur.singh@dataflowgroup.com'], from_email=from_email, bcc=[], connection=None, attachments=[], headers={}, cc=[], reply_to=[], fail_silently=False)

        return HttpResponse('')
    return render(request, 'employee/coursestarted.html', {'recommendation_count': recommendation_count, 'rating_flag': rating_flag, 'email': email,'course': course, 'scenarios': scenarios, 'course_name': cname, 'scenarios_all': scenarios_all, 'course_status': course_status, 'first_name': first_name, 'expiration_date': expiration_date, 'date_today': date_today, 'teststart_status': teststart_status, 'course_and_quest':course_and_quest, 'completed_modules': completed_modules, 'testgiven_status': testgiven_status, 'total_mod_count': total_modules, 'completed_mod_count': len(completed_modules), 'quest_answer': quest_answer})

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
@csrf_exempt
def courseprogress(request, cname, mname):
    if request.method == 'POST':
        email = request.user.email
        confidence_meter = request.POST.get(f'confidence_meter__{mname}')
        # person_team = Progress.objects.get(person_email=email, course_name=cname).person_team
        if CompletedModuledetail.objects.filter(person_email=email, course_name=cname, completed_module=mname).exists():
            comp_mod = CompletedModuledetail.objects.get(person_email=email, course_name=cname,
                                                         completed_module=mname)
            comp_mod.module_confidence = confidence_meter
            comp_mod.save()
        else:
            CompletedModuledetail.objects.create(person_email=email, course_name=cname, completed_module=mname, module_status='Active', module_confidence=confidence_meter)
        return redirect('employee:coursestarted', cname=cname)
    return redirect('show:detail', cname=cname)


@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def finalquest(request, cname):
    employee_email = request.user.email
    entry_email = employee_email
    first_name = request.user.first_name
    module_names_in_course = [i.module.module_name for i in Course.objects.filter(course_name__iexact=cname)]
    quest_count = Course.objects.filter(course_name__iexact=cname)[0].final_questcount
    questions = Question.objects.filter(module_name__in=module_names_in_course, flag__iexact='Active').order_by('?')[:quest_count]
    testgiven_status = Progress.objects.get(person_email=str(employee_email).lower(), course_name=cname).testgiven_status
    course_status = Progress.objects.get(person_email=str(employee_email).lower(), course_name=cname).course_status
    expiration_date = Progress.objects.get(person_email=str(employee_email).lower(), course_name=cname).expiration_date
    course = Course.objects.filter(course_name__exact=cname, module__status__iexact='Active').order_by('sequence_num')
    completed_modules = [(i.completed_module, i.module_confidence) for i in CompletedModuledetail.objects.filter(person_email__exact=employee_email, course_name__iexact=cname, module_status__iexact='Active')]
    total_modules = len(course)
    if questions:
        extension = [(i.module_name, str.split(i.quest_file.name, '.')[-1]) if i.quest_file.name != None else (i.module_name, None) for i in questions]
    else:
        extension = []
    # setting test restart flag
    test_start = Progress.objects.get(person_email=str(employee_email).lower(), course_name=cname)
    test_start.test_startflag = True
    test_start.save()
    #test time
    course_test_time = Course.objects.filter(course_name__iexact=cname)[0].test_time
    date_today = (timezone.now() + timezone.timedelta(hours=5.5)).date()

    # recommendation_count
    recommendation_count = Recommendation.objects.filter(recommended_to__iexact=entry_email, status__iexact='NoAction').count()
    date_today = (timezone.now() + timezone.timedelta(hours=5.5)).date()

    return render(request, 'employee/finalquest.html', {'entry_email': entry_email, 'course_name': cname, 'questions': questions, 'extension': extension,'testgiven_status': testgiven_status, "course_status": course_status, 'course_test_time': course_test_time, 'first_name':first_name, "expiration_date": expiration_date, 'date_today': date_today, 'completed_modules': completed_modules, 'total_modules': total_modules, 'recommendation_count': recommendation_count})

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
@csrf_exempt
def scorecal(request):
    if request.method == 'POST':
        employee_email = request.user.email
        question_count = request.POST.get('quest_count')
        course_name = request.POST.get('course_name')
        counter = 0
        for i in range(int(question_count)):
            quest_id = request.POST.get(f'ques_id_{i+1}')
            option_selected = request.POST.get(f'questAns__{i+1}')
            quest = Question.objects.filter(pk=quest_id)[0]
            if option_selected == quest.correct_option and option_selected != '':
                counter += 1
                QuestionAttempted.objects.create(person_email=employee_email, course_name=course_name, quest_id=quest_id,
                                                 option_given=option_selected, is_correct=True)
            elif option_selected == '':
                QuestionAttempted.objects.create(person_email=employee_email, course_name=course_name,
                                                 quest_id=quest_id,
                                                 option_given=option_selected, is_correct='Skipped')
            else:
                QuestionAttempted.objects.create(person_email=employee_email, course_name=course_name,
                                                 quest_id=quest_id,
                                                 option_given=option_selected, is_correct=False)
        score = math.ceil((counter/int(question_count)) * 100)
        prog = Progress.objects.get(person_email=str(employee_email).lower(), course_name=course_name)
        prog.score = score
        prog.course_completedtime = timezone.now() + timezone.timedelta(hours=5.5)
        prog.testgiven_status = True
        prog.test_startflag = False
        prog.save()
        return redirect('employee:getrating', empemail=prog.person_email, cname=prog.course_name)
    return redirect('employee:employeehome')

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
@csrf_exempt
def postscenario(request):
    if request.method == "POST":
        employee_email = request.user.email
        cname = request.POST.get('cname')
        mname = request.POST.get('mname')
        sc_id = request.POST.get('sId')
        sc_answer = request.POST.get(f'sOpt')
        obj = Scenario.objects.get(pk=sc_id)
        if obj.correctoption == sc_answer:
            is_correct = True
        else:
            is_correct = False
        PostScenario.objects.create(scinario_id=sc_id, scinario_answer=sc_answer, is_correct=is_correct, associated_course=cname, associated_module=mname, person_email=employee_email)
        return HttpResponse('')

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def getrating(request, empemail, cname):
    entry_email = request.user.email
    first_name = request.user.first_name
    testgiven_status = Progress.objects.get(person_email=str(empemail).lower(), course_name=cname).testgiven_status
    score = Progress.objects.get(person_email=str(empemail).lower(), course_name=cname).score
    # recommendation_count
    recommendation_count = Recommendation.objects.filter(recommended_to__iexact=entry_email, status__iexact='NoAction').count()
    return render(request, 'employee/rating.html', {'recommendation_count': recommendation_count,'emp_email': empemail, 'course_name': cname, 'score': score, 'testgiven_status': testgiven_status, 'first_name': first_name})


@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
@csrf_exempt
def postrating(request, empemail, cname):
    first_name = request.user.first_name
    if request.method == 'POST':
        rating = request.POST.get('rating')
        rating__remark = request.POST.get('rating__remark')
        prog = Progress.objects.get(person_email=str(empemail).lower(), course_name=cname)
        prog.rating_of_course = rating
        prog.improvement_rem = rating__remark
        prog.rating_flag = True
        prog.save()
        return redirect('employee:continuecourse', cname=cname)
    return redirect('employee:getrating', empemail=prog.person_email, cname=prog.course_name, first_name=first_name)

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def viewrecommendation(request):
    first_name = request.user.first_name
    entry_email = request.user.email
    entry_email = entry_email.lower()
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        module_count = request.POST.get('number_of_modules')
        recommended_users = request.POST.getlist('members[]')
        user_name = request.POST.get('user_name')
        user_designation = request.POST.get('user_designation')
       
        # check questions
        course_and_quest = []
        modules_in_c = [j.module.module_name for j in Course.objects.filter(course_name__iexact=course_name)]
        quest_count = Question.objects.filter(module_name__in=modules_in_c).count()
        if quest_count == 0:
            test_flag = False
        else:
            test_flag = True
            
        for i in recommended_users:
            splited_string = str.split(i, ',')
            recommended_name = splited_string[0]
            recommended_email = splited_string[1]
            recommended_designation = splited_string[2]
            if not Recommendation.objects.filter(recommended_course=course_name,recommended_to=recommended_email).exclude(status__iexact='Rejected').exists():
                # create recommendation
                Recommendation.objects.create(person_email=entry_email, recommended_course=course_name, recommended_to=recommended_email, test_flag=test_flag, module_count=module_count, recommended_to_name=recommended_name, recommended_to_designation=recommended_designation, user_name=user_name, user_designation=user_designation)
                # send_mail('Let\'s Learn More', f'Hi,\n\n\nHere is an opportunity to enhance your skills and knowledge of the processes.\n\nUse it before you lose it.\n\n\nTraining Course - {course_name}\n\n\nRegards,\nTraining Team', settings.EMAIL_HOST_USER, [recommended_email], fail_silently=False)
        messages.success(request, 'Course recommended successfuly!')
        
        return redirect('employee:continuecourse', cname=course_name)
    recommendation = Recommendation.objects.filter(recommended_to__iexact=entry_email).order_by('-pk')
    my_recommendation = Recommendation.objects.filter(person_email__iexact=entry_email).order_by('-pk')

    # recommendation_count
    recommendation_count = Recommendation.objects.filter(recommended_to__iexact=entry_email, status__iexact='NoAction').count()
    return render(request, 'employee/recommendation.html', {'recommendation_count': recommendation_count, 'first_name': first_name, 'entry_email': entry_email, 'recommendation': recommendation, 'my_recommendation': my_recommendation})

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def acceptrecommendation(request, cname, id):
    first_name = request.user.first_name
    entry_email = request.user.email
    entry_email = entry_email.lower()
    expiration_date = ''
    Recommendation.objects.filter(recommended_to__iexact=entry_email, recommended_course__iexact=cname, pk=id).update(status='Accepted')
    # AWS connection
    if socket.gethostbyname(socket.gethostname()) == '10.2.5.128' or socket.gethostbyname(socket.gethostname()) == '10.2.1.230':
        engine = create_engine('postgresql://analytics:analytics@123@ec2-34-246-108-106.eu-west-1.compute.amazonaws.com:5432/iadatabase')
        df_aws = pd.read_sql_query('select * from "headcount_master_darwinbox"', con=engine)
        df = df_aws[['Employee Name', 'Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting', 'Employee Code', '1st Level Reporting Email ID', 'Function Head Email ID']]
        df = df.loc[df['Email Id'] == entry_email, :]
    else:
        df = pd.DataFrame(columns=['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting',
                                    '2nd Level Reporting', 'Employee Code', '1st Level Reporting Email ID', 'Function Head Email ID'])
        df.loc[0] = ['Ankur', 'ankurkalakoti@gmail.com', 'Analytics', 'Noida', 'Rathore', 'agarwal', '11111', 'officialankursingh97@gmail.com', 'agarwal@mail.com']
        df.loc[1] = ['Anubhav', 'anubhav.kumar27@gmail.com', 'Analytics', 'Noida', 'Rathore', 'agarwal', '11111', 'rathore@mail.com', 'agarwal@mail.com']
        df.loc[2] = ['Ankur', 'officialankursingh97@gmail.com', 'Analytics', 'Noida', 'Rathore', 'agarwal', '11111', 'rathore@mail.com', 'agarwal@mail.com']
        df = df.loc[df['Email Id'] == entry_email, :]
    for i, j in df.iterrows():
        if not Progress.objects.filter(course_name=cname, person_email=j['Email Id']).exists():
            obj = Progress.objects.create(course_name=cname, person_email=j['Email Id'], person_team=j['Sub-Department'], person_name=j['Employee Name'], person_location=j['DF Site'], person_firstlevel=j['1st Level Reporting'], person_secondlevel=j['2nd Level Reporting'], person_empid=j['Employee Code'])
    return redirect('employee:viewrecommendation')



@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def rejectrecommendation(request, id):
    first_name = request.user.first_name
    entry_email = request.user.email
    entry_email = entry_email.lower()
    Recommendation.objects.filter(recommended_to__iexact=entry_email, pk=id).update(status='Rejected')
    return redirect('employee:viewrecommendation')

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def issueaction(request):
    entry_email = request.user.email
    entry_email = entry_email.lower()
    if request.method == 'POST':
        report_title = request.POST.get('report_title')
        report_description = request.POST.get('report_description')
        report_file = request.FILES.get('report_file')
        print('file ', report_file)
        # ReportIssue.objects.create(person_email=entry_email, report_title=report_title, report_description=report_description, report_file=report_file)
        return redirect('employee:employeehome')
    return redirect('employee:employeehome')

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def your_contribution(request):
    entry_email = request.user.email
    first_name = request.user.first_name
    process = Process.objects.all()
    contribution = Contribution.objects.filter(contributor_email__iexact=entry_email)

    # recommendation_count
    recommendation_count = Recommendation.objects.filter(recommended_to__iexact=entry_email, status__iexact='NoAction').count()
    return render(request, 'employee/your_contribution.html', {'recommendation_count': recommendation_count, 'first_name': first_name, 'entry_email': entry_email, 'process': process, 'contribution':contribution})

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
@csrf_exempt
def contribute(request):
    contributor_email = request.user.email
    first_name = request.user.first_name
    last_name = request.user.last_name
    contributor_name = first_name + ' ' + last_name
    if socket.gethostbyname(socket.gethostname()) == '10.2.5.128' or socket.gethostbyname(socket.gethostname()) == '10.2.1.230':
        engine = create_engine('postgresql://analytics:analytics@123@ec2-34-246-108-106.eu-west-1.compute.amazonaws.com:5432/iadatabase')
        df_aws = pd.read_sql_query('select * from "headcount_master_darwinbox"', con=engine)
        df = df_aws[['Employee Name', 'Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting', 'Employee Code', '1st Level Reporting Email ID', 'Function Head Email ID']]
        contributor_team = df.loc[df['Email Id'] == contributor_email, 'Sub-Department'].values[0]
    else:
        contributor_team = 'Analytics'

    if request.method == 'POST':
        title = request.POST.get('title')
        process_name = request.POST.getlist('process_name')
        process_name = ', '.join(process_name)
        case_study = request.FILES.get('case_study')
        supporting_docs = request.FILES.get('supporting_docs')

        Contribution.objects.create(contributor_email=contributor_email, contributor_name=contributor_name, contributor_team=contributor_team, title=title, process_name=process_name, case_study=case_study, supporting_docs=supporting_docs)
        # subject = 'New Course is up'
        # content = f'Are you ready to LEARN something new?\n\nWe’ve just uploaded the course today.'f'\n\nHead to studyhall to get your hands on the course- https://studyhall.dfgateway.com\n\nHappy Learning!\n\nRegards,' f'\nTraining Team'
        # from_email = 'Study Hall <studyhall@dataflowgroup.com>'
        # # send_mail(subject, content, from_email, [contributor_email], auth_user='analytics@dataflowgroup.com', fail_silently=False) 
        # # messages.success(request, 'Your case study has been submitted!')
        welcome_mail = WelcomeMail()
        from_email = 'Study Hall <studyhall@dataflowgroup.com>'
        subject = "Content Submission"
        title = "Thank you for your submission!"
        content = f"We’ve received your case study/essential training course contribution and we will be taking the next weeks to review the material.\n\n You should be receiving updates from us as soon as the review is completed.\n\n Stay tuned for emails coming from us!"
        button_label = ""
        button_link = f""
        try:
            welcome_mail.set_context(subject, title, content, button_label, button_link)
            welcome_mail.send([contributor_email], from_email=from_email, bcc=[], connection=None, attachments=[],
                headers={}, cc=[], reply_to=[], fail_silently=False)
        except:
            pass
        return redirect('employee:your_contribution')
    
    return redirect('employee:your_contribution')

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
@csrf_exempt
def dashboard(request):
    entry_email = request.user.email
    entry_email = str(entry_email).lower()
    employee_email = str(entry_email).lower()
    first_name = request.user.first_name

    # recommendation_count
    recommendation_count = Recommendation.objects.filter(recommended_to__iexact=entry_email, status__iexact='NoAction').count()

    # on server
    if socket.gethostbyname(socket.gethostname()) == '10.2.5.128' or socket.gethostbyname(socket.gethostname()) == '10.2.1.230':
        engine = create_engine('postgresql://analytics:analytics@123@ec2-34-246-108-106.eu-west-1.compute.amazonaws.com:5432/iadatabase')
        df_aws = pd.read_sql_query('select * from "headcount_master_darwinbox"', con=engine)
        df = df_aws[['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting', 'Employee Code', '1st Level Reporting Email ID', 'Function Head Email ID', 'Designation']]
        df['Email Id'] = df['Email Id'].str.lower()
        try:
            teams = set([i for i in df['Sub-Department']])
            user_designation=df[df['Email Id']==employee_email]['Designation'].values[0]
            user_name=df[df['Email Id']==employee_email]['Employee Name'].values[0]
            not_a_user = False
        except:
            teams = ''
            user_designation = ''
            user_name = ''
            not_a_user = True

        df_all = df
        df = df.loc[(df['1st Level Reporting Email ID'] == entry_email) | (df['Function Head Email ID'] == entry_email) | (df['Email Id'] == entry_email), :]
        if len(df):
            employee_detail_dict = [tuple(x) for x in df[['Employee Name', 'Email Id', 'Designation', 'Sub-Department']].to_numpy()]
            all_under_employees = [i[1] for i in employee_detail_dict]
        else:
            employee_detail_dict = []
            all_under_employees = []
    # on development
    else:
        df = pd.DataFrame(columns=['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting',
                                    '2nd Level Reporting', 'Employee Code', '1st Level Reporting Email ID', 'Function Head Email ID', 'Designation'])
        df.loc[0] = ['Ankur singh', 'ankurkalakoti@gmail.com', 'Analytcs', 'Noida', 'Rathore', 'agarwal', '11111', 'officialankursingh97@gmail.com', 'agarwal@mail.com', 'Associate II']
        df.loc[1] = ['Anubhav kumar', 'anubhav.kumar27@gmail.com', 'Analytcs', 'Noida', 'Rathore', 'agarwal', '11111', 'ankurkalakoti@gmail.com.com', 'princeroyale72@gmail.com', 'Associate I']
        df.loc[2] = ['OFFANKUR 2', 'Officialankursingh97@gmail.com', 'Analytcs', 'Noida', 'Rathore', 'agarwal', '11111', 'ankurkalakoti@gmail.com', 'agarwal@mail.com', 'Associate I']
        df['Email Id'] = df['Email Id'].str.lower()
        df.loc[3] = ['Raghav', 'princeroyale72@gmail.com', 'Analytcs', 'Noida', 'Rathore', 'agarwal', 'a5656', 'officialankursingh97@gmail.com', 'agarwal@mail.com', 'Associate II']
        try:
            teams = set([i for i in df['Sub-Department']])
            user_designation=df[df['Email Id']==employee_email]['Designation'].values[0]
            user_name=df[df['Email Id']==employee_email]['Employee Name'].values[0]
            not_a_user = False
        except:
            teams = ''
            user_designation = ''
            user_name = ''
            not_a_user = True

        df_all = df
        df = df.loc[(df['1st Level Reporting Email ID'] == entry_email) | (df['Function Head Email ID'] == entry_email) | (df['Email Id'] == entry_email), :]
        if len(df):
            employee_detail_dict = [tuple(x) for x in df[['Employee Name', 'Email Id', 'Designation', 'Sub-Department']].to_numpy()]
            all_under_employees = [i[1] for i in employee_detail_dict]
        else:
            employee_detail_dict = []
            all_under_employees = []

    all_under_employees.append(entry_email)

    tableInfo = Progress.objects.filter(person_email__in=all_under_employees).values()
    for i in tableInfo:
        total_mods = Course.objects.filter(course_name__iexact=i['course_name'])
        total_mods_name = [i.module.module_name for i in total_mods]
        completed_mods = [i.completed_module for i in CompletedModuledetail.objects.filter(course_name__exact=i['course_name'], person_email__iexact=i['person_email'])]
        pending_mods_name = [i for i in total_mods_name if i not in completed_mods]
        i['total_mods_name'] = total_mods_name
        i['completed_mods'] = completed_mods
        i['pending_mods_name'] = ', '.join(pending_mods_name)

        try:
            i['pending_mods'] = total_mods.count() - i['module_completed']
        except:
            i['pending_mods'] = 'Error'
        
        mods_in_c = [i.module.module_name for i in Course.objects.select_related('module').filter(course_name__exact=i['course_name'])]
        ques_in_c = Question.objects.filter(module_name__in=mods_in_c).count()
        i['ques_in_c'] = ques_in_c
        i['score_after_test'] = i['score'] if ques_in_c > 0 else 'NA'
        i['is_test_avail'] = True if ques_in_c > 0 else False
        if i['progress'] == 100:
            if ques_in_c == 0 or ques_in_c > 0 and i['testgiven_status'] == True:
                i['is_completed'] = 'Completed'
            elif ques_in_c > 0 and i['testgiven_status'] == False:
                i['is_completed'] = 'Pending'
        else:
            i['is_completed'] = 'Pending'


    if request.method == 'POST':
        selected_users = request.POST.getlist('user_search[]')
        tableInfo = Progress.objects.filter(person_email__in=selected_users).values()
        for i in tableInfo:
            total_mods = Course.objects.filter(course_name__iexact=i['course_name'])
            total_mods_name = [i.module.module_name for i in total_mods]
            completed_mods = [i.completed_module for i in CompletedModuledetail.objects.filter(course_name__exact=i['course_name'], person_email__iexact=i['person_email'])]
            pending_mods_name = [i for i in total_mods_name if i not in completed_mods]
            i['total_mods_name'] = total_mods_name
            i['completed_mods'] = completed_mods
            i['pending_mods_name'] = ''.join(pending_mods_name)
            
            try:
                i['pending_mods'] = total_mods.count() - i['module_completed']
            except:
                i['pending_mods'] = 'Error'
        
            mods_in_c = [i.module.module_name for i in Course.objects.select_related('module').filter(course_name__exact=i['course_name'])]
            ques_in_c = Question.objects.filter(module_name__in=mods_in_c).count()
            i['ques_in_c'] = ques_in_c
            i['score_after_test'] = i['score'] if ques_in_c > 0 else 'NA'
            i['is_test_avail'] = True if ques_in_c > 0 else False
            if i['progress'] == 100:
                if ques_in_c == 0 or ques_in_c > 0 and i['testgiven_status'] == True:
                    i['is_completed'] = 'Completed'
                elif ques_in_c > 0 and i['testgiven_status'] == False:
                    i['is_completed'] = 'Pending'
            else:
                i['is_completed'] = 'Pending'

        total_enrolled_courses = len(Progress.objects.filter(person_email__in=selected_users).values())
        active_courses = len([i for i in tableInfo if i['is_completed'] == 'Pending'])
        completed_courses = total_enrolled_courses - active_courses
        course_and_score = [(i['course_name'], i['score']) for i in tableInfo if i['is_test_avail'] == True and i['is_completed'] == 'Completed']
        try:
            avg_score = sum(i[1] for i in course_and_score)/len(course_and_score)
        except:
            avg_score = 0

        if len(employee_detail_dict) == 1:
            if str(entry_email) == 'ankur.singh@dataflowgroup.com':
                search_on = False
                employee_detail_dict.append(('Sanjeev R', 'sanjeev.rathore@dataflowgroup.com', 'Manager', 'Analytcs'))
            elif employee_detail_dict[0][1] == entry_email:
                search_on = True
        else:
            search_on = False

        # recommendation_count
        recommendation_count = Recommendation.objects.filter(recommended_to__iexact=entry_email, status__iexact='NoAction').count()
        renderObj = {'first_name': first_name, 'entry_email': entry_email, 'employee_detail_dict': employee_detail_dict, 'tableInfo': tableInfo, 'recommendation_count': recommendation_count, 'total_enrolled_courses': total_enrolled_courses, 'active_courses': active_courses, 'completed_courses': completed_courses, 'avg_score': avg_score, 'search_on': search_on}
        return render(request, 'employee/dashboard.html', renderObj)


    if len(employee_detail_dict) == 1:
        if str(entry_email) == 'ankur.singh@dataflowgroup.com':
            search_on = False
            employee_detail_dict.append(('Sanjeev R', 'sanjeev.rathore@dataflowgroup.com', 'Manager', 'Analytcs'))
        elif employee_detail_dict[0][1] == entry_email:
            search_on = True
    else:
        search_on = False
    

    total_enrolled_courses = len(Progress.objects.filter(person_email__in=all_under_employees).values())
    active_courses = len([i for i in tableInfo if i['is_completed'] == 'Pending'])
    completed_courses = total_enrolled_courses - active_courses
    course_and_score = [(i['course_name'], i['score']) for i in tableInfo if i['is_test_avail'] == True and i['is_completed'] == 'Completed']
    try:
        avg_score = sum(i[1] for i in course_and_score)/len(course_and_score)
    except:
        avg_score = 0    
    renderObj = {'first_name': first_name, 'entry_email': entry_email, 'employee_detail_dict': employee_detail_dict, 'recommendation_count': recommendation_count, 'search_on': search_on, 'tableInfo': tableInfo, 'total_enrolled_courses': total_enrolled_courses, 'active_courses': active_courses, 'completed_courses': completed_courses, 'avg_score': avg_score}
    return render(request, 'employee/dashboard.html', renderObj)
