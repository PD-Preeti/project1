from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.contrib.auth import logout, login
from django.contrib import messages
from django.conf import settings
from adminboard.models import Course, Module, AuthorizedPanel, Scenario, Question, Process
from django.views.decorators.csrf import csrf_exempt
from employee.models import Progress, CompletedModuledetail, QuestionAttempted, PostScenario, Contribution, QnA
import json
import pandas as pd
from datetime import datetime, timedelta
from django.db.models import Avg
from sqlalchemy.engine import create_engine
from django.core.mail import send_mail
import socket
from django.db.models.functions import Lower
from adminboard.mails import WelcomeMail
from django.contrib.auth import authenticate, login


def loginadmin(request):
    settings.LOGIN_REDIRECT_URL = '/adminboard/adminhome/'
    return render(request, 'adminboard/login.html')

@csrf_exempt
def loginadminuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_adminuser = request.POST.get('login_adminuser')
        adminuser = authenticate(username=username, password=password)
        if adminuser is not None:
            login(request, adminuser)
            if login_adminuser == "adminboard":
                return redirect('adminboard:adminhome')
            elif login_adminuser == 'studyhall':
                return redirect('employee:employeehome')
        else:
            return render(request, 'adminboard/loginadminuser.html')
    return render(request, 'adminboard/loginadminuser.html')

def authentication_check(user):
    return user.is_authenticated

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def adminhome(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    courses = Course.objects.order_by().values('course_name', 'course_status').distinct()

    c_assigned_completed = []
    for i in courses:
        total_assigned = len(Progress.objects.filter(course_name__iexact=i['course_name']))
        total_completed = len(Progress.objects.filter(course_name__iexact=i['course_name'], progress=100))
        c_assigned_completed.append((i['course_name'], total_assigned, total_completed))
    #expired courses
    expired_courses = Progress.objects.filter(expiration_date__lt=datetime.now().date())
    #pending_courses
    # pending_courses = Progress.objects.filter(testgiven_status=False, course_status__iexact='active')
    all_completed = len(Progress.objects.filter(progress=100))
    all_courses = len(Progress.objects.all())
    pending_courses = all_courses - all_completed
    #overall_avg_score
    overall_avg_score = Progress.objects.all().aggregate(Avg('score'))['score__avg']
    course_cover = []
    for i in courses:
        course_cover = Course.objects.filter(course_name__iexact=i['course_name'])[0].course_cover
        i['course_cover'] = course_cover

    #avg score per course
    all_assingned_avg_rating = Progress.objects.filter(rating_flag=True).values('course_name').annotate(avg_rating=Avg('rating_of_course'))
    return render(request, 'adminboard/home.html', {'courses': courses, 'entry_email': entry_email, 'admin_emails': admin_emails, 'all_assingned_avg_rating': all_assingned_avg_rating, 'course_cover': course_cover,
                                                    'pending_courses_count': pending_courses, 'overall_avg_score': overall_avg_score,
                                                    'c_assigned_completed': c_assigned_completed, 'expired_courses_count': len(expired_courses)})


@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def logout_admin(request):
    logout(request)
    return redirect('adminboard:loginadmin')

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
@csrf_exempt
def savemodule(request):
    entry_email = request.user.email
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    if entry_email in admin_emails:
        if 'submit' in request.POST:
            course_name = request.POST.get('coursename')
            module_name = request.POST.get('modname')
            process_name = request.POST.getlist('process')
            location = request.POST.getlist('location')
            file1 = request.FILES.get('modfile1')
            file2 = request.FILES.get('modfile2')
            video_file = request.FILES.get('video_file')
            file3 = request.FILES.get('modfile3')
            file4 = request.FILES.get('modfile4')
            file5 = request.FILES.get('modfile5')
            file6 = request.FILES.get('modfile6')
            file7 = request.FILES.get('modfile7')
            file8 = request.FILES.get('modfile8')
            file9 = request.FILES.get('modfile9')
            file10 = request.FILES.get('modfile10')
            file11 = request.FILES.get('modfile11')
            file12 = request.FILES.get('modfile12')
            file13 = request.FILES.get('modfile13')
            file14 = request.FILES.get('modfile14')
            link1 = request.POST.get('link1')
            link2 = request.POST.get('link2')
            link3 = request.POST.get('link3')
            link4 = request.POST.get('link4')
            link5 = request.POST.get('link5')
            link6 = request.POST.get('link6')
            link7 = request.POST.get('link7')
            link8 = request.POST.get('link8')
            link9 = request.POST.get('link9')
            link10 = request.POST.get('link10')
            process_name = ', '.join(process_name)
            location = ', '.join(location)
            if Course.objects.filter(course_name__iexact=course_name).exists():
                course = Course.objects.get(course_name=course_name)
                Module.objects.create(course=course, module_name=module_name, video_file=video_file,
                                      file1=file1, file2=file2, file3=file3, file4=file4, file5=file5, file6=file6, 
                                      file7=file7, file8=file8, file9=file9, file10=file10, file11=file11, file12=file12, file13=file13, file14=file14, process_name=process_name, location=location, 
                                      link1=link1, link2=link2, link3=link3, link4=link4, link5=link5,
                                       link6=link6, link7=link7, link8=link8, link9=link9, link10=link10)
            elif Module.objects.filter(module_name__iexact=module_name).exists():
                messages.success(request, 'Module already present!')
            else:
                Module.objects.create(module_name=module_name,
                                      file1=file1, file2=file2,  file3=file3, file4=file4, file5=file5, file6=file6, 
                                      file7=file7, file8=file8, file9=file9, file10=file10, file11=file11, file12=file12, process_name=process_name, location=location, link1=link1, 
                                      link2=link2, link3=link3, link4=link4, link5=link5, video_file=video_file,
                                       link6=link6, link7=link7, link8=link8, link9=link9, link10=link10)
                messages.success(request, 'Module created successfuly!')
            return redirect('adminboard:addmodule')
        elif 'save' in request.POST:
            course_name = request.POST.get('coursename')
            module_name = request.POST.get('modname')
            process_name = request.POST.getlist('process')
            location = request.POST.getlist('location')
            id = request.POST.get('id')

            file1 = request.FILES.get('modfile1')
            if file1 is None:
                file1 = Module.objects.filter(pk=id)[0].file1
                
            file2 = request.FILES.get('modfile2')
            if file2 is None:
                file2 = Module.objects.filter(pk=id)[0].file2

            video_file = request.FILES.get('video_file')
            if video_file is None:
                video_file = Module.objects.filter(pk=id)[0].video_file

            file3 = request.FILES.get('modfile3')
            if file3 is None:
                file3 = Module.objects.filter(pk=id)[0].file3

            file4 = request.FILES.get('modfile4')
            if file4 is None:
                file4 = Module.objects.filter(pk=id)[0].file4

            file5 = request.FILES.get('modfile5')
            if file5 is None:
                file5 = Module.objects.filter(pk=id)[0].file5

            file6 = request.FILES.get('modfile6')
            if file6 is None:
                file6 = Module.objects.filter(pk=id)[0].file6

            file7 = request.FILES.get('modfile7')
            if file7 is None:
                file7 = Module.objects.filter(pk=id)[0].file7

            file8 = request.FILES.get('modfile8')
            if file8 is None:
                file8 = Module.objects.filter(pk=id)[0].file8

            file9 = request.FILES.get('modfile9')
            if file9 is None:
                file9 = Module.objects.filter(pk=id)[0].file9

            file10 = request.FILES.get('modfile10')
            if file10 is None:
                file10 = Module.objects.filter(pk=id)[0].file10

            file11 = request.FILES.get('modfile11')
            if file11 is None:
                file11 = Module.objects.filter(pk=id)[0].file11

            file12 = request.FILES.get('modfile12')
            if file12 is None:
                file12 = Module.objects.filter(pk=id)[0].file12

            file13 = request.FILES.get('modfile13')
            if file13 is None:
                file13 = Module.objects.filter(pk=id)[0].file13

            file14 = request.FILES.get('modfile14')
            if file14 is None:
                file14 = Module.objects.filter(pk=id)[0].file14

            link1 = request.POST.get('link1')
            link2 = request.POST.get('link2')
            link3 = request.POST.get('link3')
            link4 = request.POST.get('link4')
            link5 = request.POST.get('link5')
            link6 = request.POST.get('link6')
            link7 = request.POST.get('link7')
            link8 = request.POST.get('link8')
            link9 = request.POST.get('link9')
            link10 = request.POST.get('link10')
            process_name = ', '.join(process_name)
            location = ', '.join(location)

            Module.objects.filter(pk=id).update(module_name=module_name, video_file=video_file,
                                      file1=file1, file2=file2, file3=file3, file4=file4, file5=file5, file6=file6, 
                                      file7=file7, file8=file8, file9=file9, file10=file10, file11=file11, file12=file12, file13=file13, file14=file14, process_name=process_name, location=location, 
                                      link1=link1, link2=link2, link3=link3, link4=link4, link5=link5,
                                       link6=link6, link7=link7, link8=link8, link9=link9, link10=link10)

            messages.success(request, 'Module updated successfuly!')
            return redirect('adminboard:viewmodule')
    else:
        return render(request, 'adminboard/notauthorized_admin.html')


@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def visitmodule(request, modname):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    module = Module.objects.get(module_name=modname)
    if module.file1 is not None:
        file1 = str.split(module.file1.name, '.')[-1]
    if module.file2 is not None:
        file2 = str.split(module.file2.name, '.')[-1]
    if module.video_file is not None:
        video_file = str.split(module.video_file.name, '.')[-1]
    file3 = str.split(module.file3.name, '.')[-1] if module.file3 else ''
    file4 = str.split(module.file4.name, '.')[-1] if module.file4 else ''
    file5 = str.split(module.file5.name, '.')[-1] if module.file5 else ''
    file6 = str.split(module.file6.name, '.')[-1] if module.file6 else ''
    file7 = str.split(module.file7.name, '.')[-1] if module.file7 else ''
    file8 = str.split(module.file8.name, '.')[-1] if module.file8 else ''
    file9 = str.split(module.file9.name, '.')[-1] if module.file9 else ''
    file10 = str.split(module.file10.name, '.')[-1] if module.file10 else ''
    file11 = str.split(module.file11.name, '.')[-1] if module.file11 else ''
    file12 = str.split(module.file12.name, '.')[-1] if module.file12 else ''
    file13 = str.split(module.file13.name, '.')[-1] if module.file13 else ''
    file14 = str.split(module.file14.name, '.')[-1] if module.file14 else ''
    extension = (file1, file2, video_file, file3, file4, file5, file6, file7, file8, file9, file10, file11, file12, file13, file14)
    scenarios = Scenario.objects.filter(associated_module__iexact=module.module_name, flag__iexact='Active')
    quest_per_mod = Question.objects.filter(module_name__iexact=modname, flag__iexact='Active').order_by('-id')
    return render(request, 'adminboard/visitMod.html', {'module': module, 'entry_email': entry_email, 'admin_emails': admin_emails, 'scenarios': scenarios, 'quest_per_mod': quest_per_mod, 'extension':extension})


@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def createcourse(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    # print(admin_emails)
    module = Module.objects.filter(status__iexact='Active').order_by(Lower('module_name'))
    # print(module)
    course_names = Course.objects.values('course_name').distinct()
    module_dict = {}
    for index, i in enumerate(module):
        print(i.module_name)
        module_dict[index] = i.module_name
    module_dict = json.dumps(module_dict)
    # print(module_dict)
    # on server
    if socket.gethostbyname(socket.gethostname()) == '10.2.5.128' or socket.gethostbyname(socket.gethostname()) == '10.2.1.230':
        engine = create_engine('postgresql://analytics:analytics@123@ec2-34-246-108-106.eu-west-1.compute.amazonaws.com:5432/iadatabase')
        df_aws = pd.read_sql_query('select * from "headcount_master_darwinbox"', con=engine)
        df = df_aws[['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting', 'Employee Code']]
        teams = set([i for i in df['Sub-Department']])
        notify_users = list(zip(df['Employee Name'], df['Email Id'], df['Sub-Department'], df['DF Site'], df['1st Level Reporting'], df['2nd Level Reporting'], df['Employee Code']))
    # on development
    else:
        df = pd.DataFrame(columns = ['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting', 'Employee Code'])
        df.loc[0] = ['Ankur', 'ankurkalakoti@gmail.com', 'IT', 'Noida', 'Rathore', 'agarwal', '11111']
        df.loc[1] = ['Anubhav', 'anubhav.kumar27@gmail.com', 'Analytics', 'Noida', 'Rathore', 'agarwal', '11111']
        df.loc[2] = ['Hind', 'hind@gmail.com', 'Audit', 'Noida', 'Rathore', 'agarwal', '11111']
        teams = set([i for i in df['Sub-Department']])
        notify_users = list(zip(df['Employee Name'], df['Email Id'], df['Sub-Department'], df['DF Site'], df['1st Level Reporting'], df['2nd Level Reporting'], df['Employee Code']))
    return render(request, 'adminboard/createcourse.html', {'admin_emails': admin_emails, 'entry_email': entry_email, 'module_dict': module_dict, 'course_names':course_names, 'teams': teams, 'notify_users':notify_users})


@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def addmodule(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    process_name = Process.objects.all()
    locations = ['Mumbai', 'Amman', 'Noida', 'Hyderabad', 'Dubai', 'Bangkok',
       'Singapore City', 'Manila', 'London', 'Cairo', 'Berlin', 'Kochi',
       'Kuala Lumpur', 'Doha', 'Manama', 'Riyadh']
    modules = [i.lower() for i in Module.objects.values_list('module_name', flat=True).distinct()]
    return render(request, 'adminboard/addMod.html', {'modules': modules, 'locations': locations, 'process_name': process_name, 'entry_email': entry_email, 'admin_emails': admin_emails})

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def viewmodule(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    module = Module.objects.filter(status__iexact='Active')
    module_list = [i.module_name for i in module]
    courses = [i.course_name for i in Course.objects.filter(module__module_name__in=module_list)]

    progress = Progress.objects.filter(course_name__in=courses).filter(testgiven_status=False)

    course_in_incomplete_progress = list(set([i.course_name for i in progress]))

    completed_modules = [i.module_completedtime for i in CompletedModuledetail.objects.filter(course_name__in=course_in_incomplete_progress).exclude(module_status__iexact='Archived')]
    total_mods = [i.module_name for i in Module.objects.filter(status__iexact='Active')]
    assigned_mod = list(set([i.module.module_name for i in Course.objects.filter(course_name__in=course_in_incomplete_progress)]))
    not_assigned_mods = [i for i in total_mods if i not in assigned_mod]
    incomplete_module = [i.module.module_name for i in Course.objects.exclude(module__module_name__in=completed_modules)]
    incomplete_modules = [i for i in incomplete_module if i not in not_assigned_mods]
    return render(request, 'adminboard/viewMod.html', {'incomplete_modules': incomplete_modules, 'entry_email': entry_email, 'admin_emails': admin_emails, 'module': module})

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def visitcourse(request, cname):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    module = [i.module for i in Course.objects.filter(course_name__iexact=cname).order_by('sequence_num')]  
    all_mod_exc_present = Module.objects.filter(status__iexact='Active').exclude(module_name__in=module)
    all_mod_incourse = Module.objects.filter(module_name__in=module, status__iexact='Active')
    module_dict = {}
    for i in all_mod_exc_present:
        module_dict[i.id] = i.module_name
    module_dict = json.dumps(module_dict)
    module_dict_present = {}
    for i in all_mod_incourse:
        module_dict_present[i.id] = i.module_name
    module_dict_present = json.dumps(module_dict_present)
    module_names_in_course = [i.module.module_name for i in Course.objects.filter(course_name__iexact=cname)]
    questions = Question.objects.filter(module_name__in=module_names_in_course, flag__iexact='Active').distinct()
    course_status = Course.objects.filter(course_name__iexact=cname)[0].course_status
    return render(request, 'adminboard/visitcourse.html', {'entry_email': entry_email, 'admin_emails': admin_emails, 'module': module, 'questions': questions, 'course_status': course_status,
                                                            'course': cname, 'all_mod_exc_present': all_mod_exc_present, 'module_dict': module_dict, 'module_dict_present': module_dict_present})


@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
@csrf_exempt
def savecourse(request):
    person_name = request.user.first_name
    person_email = request.user.email

    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        json_items = request.POST.get('json_items')
        course_team = request.POST.getlist('course_team')
        course_team = ', '.join(course_team)
        course_test_time = request.POST.get('course_test_time')
        course_cover = request.FILES.get('cover')
        module_names = str.split(json_items, ',')
        final_questcount = request.POST.get('course_test_quest')
        notify_to = request.POST.get('notify_to')
        
        messages.success(request, 'Course created successfuly!')

        for index, i in enumerate(module_names):
            try:
                mod = Module.objects.get(module_name=i)
                Course.objects.create(course_name=course_name, module=mod, sequence_num=index+1, id_of_module=mod.id, test_time=abs(int(course_test_time)), course_cover=course_cover, course_status='Active', final_questcount=final_questcount, course_team=course_team)
            except:
                return HttpResponse(f'<h1>Module {i} not found</h1>')

        if notify_to != None:
            if notify_to == 'notify_teams':
                notify_teams = request.POST.getlist('notify_teams_tags[]')
                # on server
                if socket.gethostbyname(socket.gethostname()) == '10.2.5.128' or socket.gethostbyname(socket.gethostname()) == '10.2.1.230':
                    engine = create_engine('postgresql://analytics:analytics@123@ec2-34-246-108-106.eu-west-1.compute.amazonaws.com:5432/iadatabase')
                    df_aws = pd.read_sql_query('select * from "headcount_master_darwinbox"', con=engine)
                    df = df_aws[['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting', 'Employee Code']]
                    teams = set([i for i in df['Sub-Department']])
                # on development
                else:
                    df = pd.DataFrame(columns = ['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting', 'Employee Code'])
                    df.loc[0] = ['Ankur', 'ankurkalakoti@gmail.com', 'IT', 'Noida', 'Rathore', 'agarwal', '11111']
                    df.loc[1] = ['Ankur Singh', 'ankur.singh@dataflowgroup.com', 'Analytics', 'Noida', 'S Rathore', 'S Agarwal', '11111']
                    df.loc[2] = ['Hind', 'hind@gmail.com', 'Audit', 'Noida', 'Rathore', 'agarwal', '11111']
                    teams = set([i for i in df['Sub-Department']])
                for i in notify_teams:
                    users_of_team = df.loc[df['Sub-Department'] == i, :]
                    emails_of_team = [str(i).lower() for i in users_of_team['Email Id']]
                    for j in emails_of_team:
                        # Mail Formatter
                        welcome_mail = WelcomeMail()
                        from_email = 'studyhall@dataflowgroup.com'
                        subject = "New Course is up"
                        title = "Are you ready to LEARN something new?"
                        content = f"We’ve just uploaded the course/module {course_name} today.\n\nClick the register button below to save a seat!\n\nHappy Learning!"
                        button_label = "Register"
                        button_link = f"https://uatstudyhall.dfgateway.com/continuecourse/{course_name}/"
                        welcome_mail.set_context(subject, title, content, button_label, button_link)
                        welcome_mail.send([j], from_email=from_email, bcc=[], connection=None, attachments=[],
                            headers={}, cc=[], reply_to=[], fail_silently=False)
            else:
                users_to_notify = request.POST.getlist('notify_users_tags[]') 
                for i in users_to_notify:
                    # Mail Formatter
                    welcome_mail = WelcomeMail()
                    from_email = 'studyhall@dataflowgroup.com'
                    subject = "New Course is up"
                    title = "Are you ready to LEARN something new?"
                    content = f"We’ve just uploaded the course/module {course_name} today.\n\nClick the register button below to save a seat!\n\nHappy Learning!"
                    button_label = "Register"
                    button_link = f"https://uatstudyhall.dfgateway.com/continuecourse/{course_name}/"

                    welcome_mail.set_context(subject, title, content, button_label, button_link)
                    welcome_mail.send([i], from_email=from_email, bcc=[], connection=None, attachments=[],
                        headers={}, cc=[], reply_to=[], fail_silently=False)

        return redirect('adminboard:createcourse')
    return redirect('adminboard:createcourse')

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def editcourse(request, cname):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    module = [i.module for i in Course.objects.filter(course_name__iexact=cname).order_by('sequence_num')]
    all_mod_exc_present = Module.objects.filter(status__iexact='Active').exclude(module_name__in=module)
    all_mod_incourse = Module.objects.filter(module_name__in=module, status__iexact='Active')
    module_dict = {}
    for i in all_mod_exc_present:
        module_dict[i.id] = i.module_name
    module_dict = json.dumps(module_dict)
    module_dict_present = {}
    for i in all_mod_incourse:
        module_dict_present[i.id] = i.module_name
    module_dict_present = json.dumps(module_dict_present)
    course_time = Course.objects.filter(course_name__iexact=cname)[0].test_time
    course_quest = Course.objects.filter(course_name__iexact=cname)[0].final_questcount
    course_team = Course.objects.filter(course_name__iexact=cname)[0].course_team
    print(course_team)
    course_names = Course.objects.values('course_name').distinct()
    # teams
    if socket.gethostbyname(socket.gethostname()) == '10.2.5.128' or socket.gethostbyname(socket.gethostname()) == '10.2.1.230':
        engine = create_engine('postgresql://analytics:analytics@123@ec2-34-246-108-106.eu-west-1.compute.amazonaws.com:5432/iadatabase')
        df_aws = pd.read_sql_query('select * from "headcount_master_darwinbox"', con=engine)
        df = df_aws[['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting', 'Employee Code']]
        teams = set([i for i in df['Sub-Department']])
    # on development
    else:
        df = pd.DataFrame(columns = ['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting', 'Employee Code'])
        df.loc[0] = ['Ankur', 'ankurkalakoti@gmail.com', 'IT', 'Noida', 'Rathore', 'agarwal', '11111']
        df.loc[1] = ['Anubhav', 'anubhav.kumar27@gmail.com', 'Analytics', 'Noida', 'Rathore', 'agarwal', '11111']
        df.loc[2] = ['Hind', 'hind@gmail.com', 'Audit', 'Noida', 'Rathore', 'agarwal', '11111']
        teams = set([i for i in df['Sub-Department']])
    
    return render(request, 'adminboard/editcourse.html', {'entry_email': entry_email, 'admin_emails': admin_emails, 'module': module, 'course_time': course_time, 'course_team': course_team, 'course_names':course_names, 'course': cname, 'all_mod_exc_present': all_mod_exc_present, 'module_dict': module_dict, 'module_dict_present': module_dict_present, 'course_quest': course_quest, 'teams':teams})

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
@csrf_exempt
def updatecourse(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_team = request.POST.getlist('course_team')
        course_team = ', '.join(course_team)
        json_items = request.POST.get('json_items')
        course_test_time = request.POST.get('course_test_time')
        course_cover = request.FILES.get('cover')
        module_names = str.split(json_items, ',')
        final_questcount = request.POST.get('course_test_quest')
        created_time = Course.objects.filter(course_name__iexact=course_name)[0].created_time
        Course.objects.filter(course_name__iexact=course_name).delete()
        for index, i in enumerate(module_names):
            try:
                mod = Module.objects.get(module_name=i)
            except:
                return HttpResponse(f'<h1>Module {i} not found</h1>')
            if course_cover != '':
                Course.objects.create(course_name=course_name, module=mod, sequence_num=index + 1, id_of_module=mod.id, test_time=course_test_time, course_cover=course_cover, course_status='Active', course_team=course_team, final_questcount=final_questcount, updated_time=datetime.now() + timedelta(hours=5.5), created_time=created_time)
            else:
                Course.objects.create(course_name=course_name, module=mod, sequence_num=index + 1, id_of_module=mod.id, test_time=course_test_time, course_status='Active', course_team=course_team,
                final_questcount=final_questcount, updated_time=datetime.now() + timedelta(hours=5.5), created_time=created_time)
        messages.success(request, 'Course edited successfuly!')
        return redirect('adminboard:adminhome')
    return redirect('adminboard:adminhome')


@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def casestudy(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    modules = Module.objects.filter(status__iexact='Active')
    return render(request, 'adminboard/caseStudy.html', {'entry_email': entry_email, 'admin_emails': admin_emails, 'modules': modules})


@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def finalquest(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    modules = Module.objects.filter(status__iexact='active')
    return render(request, 'adminboard/finalquest.html', {'entry_email': entry_email, 'admin_emails': admin_emails, 'modules': modules})

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
@csrf_exempt
def postscenario(request):
    if 'submit' in request.POST:
        scenario = request.POST.get('scenario')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct = request.POST.get('correct')
        assocMod = request.POST.getlist('assoc[]')
        reason = request.POST.get('reason')
        scenario__media = request.FILES.get('scenario__media')
        for i in assocMod:
            Scenario.objects.create(scenario_desc=scenario, option1=option1, option2=option2, scenario_file=scenario__media,
                                    option3=option3, option4=option4, correctoption=correct, associated_module=i, reason=reason)
        messages.success(request, 'Scenario created successfuly!')
        return redirect('adminboard:casestudy')
    elif 'update' in request.POST:
        sc_id = request.POST.get('id')
        scenario = request.POST.get('scenario')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct = request.POST.get('correct')
        assocMod = request.POST.getlist('assoc[]')
        reason = request.POST.get('reason')
        scenario__media = request.FILES.get('scenario__media')
        sc_dec = Scenario.objects.get(pk=sc_id).scenario_desc
        sc_doc = Scenario.objects.get(pk=sc_id).scenario_file
        sc_objs = Scenario.objects.filter(scenario_desc__exact=sc_dec)
        present_mod = [i.associated_module for i in sc_objs]
        to_update = list(set(present_mod) & set(assocMod))
        to_add = list(set(assocMod) - set(present_mod))
        to_delete = list(set(present_mod) - set(assocMod))
        # print(to_update)
        # print(to_add)
        # print(set(present_mod) - set(assocMod))
        sc_objs.filter(associated_module__in=to_delete).delete()
        for i in to_update:
            if scenario__media == None:
                sc_objs.filter(associated_module__exact=i).update(scenario_desc=scenario, option1=option1, option2=option2,
                    option3=option3, option4=option4, correctoption=correct, reason=reason)
            else:
                sc_objs.filter(associated_module__exact=i).update(scenario_desc=scenario,
                 option1=option1, option2=option2, scenario_file=scenario__media,
                    option3=option3, option4=option4, correctoption=correct, reason=reason)
        for i in to_add:
            if scenario__media == None:
                Scenario.objects.create(scenario_desc=scenario, option1=option1, option2=option2, scenario_file=sc_doc,
                    option3=option3, option4=option4, correctoption=correct, associated_module=i, reason=reason)
            else:
                Scenario.objects.create(scenario_desc=scenario, option1=option1, option2=option2,
                    option3=option3, option4=option4, correctoption=correct, associated_module=i, reason=reason)
        messages.success(request, 'Scenarios updated!')
        return redirect('adminboard:getcasestudy')
    return redirect('adminboard:casestudy')

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def assign(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    courses = Course.objects.order_by().values('course_name').filter(course_status="Active").distinct()
    # get team names
    # on server
    if socket.gethostbyname(socket.gethostname()) == '10.2.5.128' or socket.gethostbyname(socket.gethostname()) == '10.2.1.230':
        engine = create_engine('postgresql://analytics:analytics@123@ec2-34-246-108-106.eu-west-1.compute.amazonaws.com:5432/iadatabase')
        df_aws = pd.read_sql_query('select * from "headcount_master_darwinbox"', con=engine)
        df = df_aws[['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting', 'Employee Code']]
        teams = set([i for i in df['Sub-Department']])
        employee_detail_dict = list(zip(df['Employee Name'], df['Email Id'], df['Sub-Department'], df['DF Site'], df['1st Level Reporting'], df['2nd Level Reporting'], df['Employee Code']))
    # on development
    else:
        df = pd.DataFrame(columns = ['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting', 'Employee Code'])
        df.loc[0] = ['Ankur', 'ankurkalakoti@gmail.com', 'Analytcs', 'Noida', 'Rathore', 'agarwal', '11111']
        df.loc[1] = ['Anubhav', 'anubhav.kumar27@gmail.com', 'Analytcs', 'Noida', 'Rathore', 'agarwal', '11111']
        teams = set([i for i in df['Sub-Department']])
        employee_detail_dict = list(zip(df['Employee Name'], df['Email Id'], df['Sub-Department'], df['DF Site'], df['1st Level Reporting'], df['2nd Level Reporting'], df['Employee Code']))
    assigned_courses = Progress.objects.exclude(course_status__iexact='deleted')
    return render(request, 'adminboard/assign.html', {'assigned_courses': assigned_courses, 'entry_email': entry_email, 'admin_emails': admin_emails, 'courses': courses, 'teams': teams,
                                                      'employee_detail_dict': employee_detail_dict, 'progress': Progress.objects.all()})

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def people(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    candidates = Progress.objects.all()
    return render(request, 'adminboard/people.html', {'entry_email': entry_email, 'admin_emails': admin_emails, 'candidates': candidates})

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
@csrf_exempt
def postquest(request):
    if 'submit' in request.POST:
        module_name = request.POST.get('module-name')
        question = request.POST.get('question')
        option1 = request.POST.get('c-option1')
        option2 = request.POST.get('c-option2')
        option3 = request.POST.get('c-option3')
        option4 = request.POST.get('c-option4')
        correct_option = request.POST.get('correct')
        quest_file = request.FILES.get('quest_file')
        Question.objects.create(module_name=module_name, question=question, option1=option1, option2=option2,
                                option3=option3, option4=option4, correct_option=correct_option, quest_file=quest_file)
        messages.success(request, 'Question created successfuly!')
        return redirect('adminboard:finalquest')
    elif 'update' in request.POST:
        quest_id = request.POST.get('id')
        module_name = request.POST.get('module-name')
        question = request.POST.get('question')
        option1 = request.POST.get('c-option1')
        option2 = request.POST.get('c-option2')
        option3 = request.POST.get('c-option3')
        option4 = request.POST.get('c-option4')
        correct_option = request.POST.get('correct')
        quest_file = request.FILES.get('quest_file')
        if quest_file == None:
            Question.objects.filter(pk=quest_id).update(module_name=module_name, question=question, option1=option1, option2=option2,
                                option3=option3, option4=option4, correct_option=correct_option)
        else:
            Question.objects.filter(pk=quest_id).update(module_name=module_name, question=question, option1=option1, option2=option2,
                                option3=option3, option4=option4, correct_option=correct_option, quest_file=quest_file)
            
        messages.success(request, 'Question updated!')
        return redirect('adminboard:getallquest')
    return redirect('adminboard:finalquest')

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
@csrf_exempt
def postassign(request):
    if request.method == 'POST':
        course_name = request.POST.get('course')
        category = request.POST.get('assign_to')
        expiration_date = request.POST.get('expired_date', None)

        if category == 'teams':
            teams = request.POST.getlist('tags[]')
            if socket.gethostbyname(socket.gethostname()) == '10.2.5.128' or socket.gethostbyname(socket.gethostname()) == '10.2.1.230':
                engine = create_engine('postgresql://analytics:analytics@123@ec2-34-246-108-106.eu-west-1.compute.amazonaws.com:5432/iadatabase')
                df_aws = pd.read_sql_query('select * from "headcount_master_darwinbox"', con=engine)
                df = df_aws[['Employee Name', 'Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting', 'Employee Code']]
            else:
                df = pd.DataFrame(columns=['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting',
                                           '2nd Level Reporting', 'Employee Code'])
                df.loc[0] = ['Ankur', 'ankurkalakoti@gmail.com', 'Analytcs', 'Noida', 'Rathore', 'agarwal', '11111']
                df.loc[1] = ['Anubhav', 'anubhav.kumar27@gmail.com', 'Analytcs', 'Noida', 'Rathore', 'agarwal', '11111']
            filter_by_teams = df['Sub-Department'].isin(teams)
            df = df[filter_by_teams]
            for i, j in df.iterrows():
                if not Progress.objects.filter(course_name=course_name, person_email=j['Email Id']).exists():
                    if expiration_date == '':
                        obj = Progress.objects.create(course_name=course_name, person_email=j['Email Id'],
                         person_team=j['Sub-Department'],
                                            person_name=j['Employee Name'][0], person_location=j['DF Site'],
                                            person_firstlevel=j['1st Level Reporting'], person_secondlevel=j['2nd Level Reporting'], person_empid=j['Employee Code'])
                    else:
                        obj = Progress.objects.create(course_name=course_name, person_email=j['Email Id'], person_team=j['Sub-Department'],
                                            person_name=j['Employee Name'][0], expiration_date=expiration_date, person_location=j['DF Site'],
                                            person_firstlevel=j['1st Level Reporting'], person_secondlevel=j['2nd Level Reporting'], person_empid=j['Employee Code'])

                    # email notification to person to which course is assigned
                    # send_mail('Let\'s Learn More', f'Dear {obj.person_name},\n\n\nHere is an opportunity to enhance your skills and knowledge of the processes.\n\nUse it before you lose it.\n\n\nTraining Course - {obj.course_name}\nExpiry Date - {obj.expiration_date}\n\n\nRegards,\nTraining Team', settings.EMAIL_HOST_USER, [obj.person_email], fail_silently=False)


            
        elif category == 'users':
            users = request.POST.getlist('tags2[]')
            trigger_email = request.POST.get("trigger_email")
            print(trigger_email)
            for i in users:
                splited_string = str.split(i, ',')
                employee_name = splited_string[0]
                employee_email = splited_string[1]
                team_name = splited_string[2]
                location = splited_string[3]
                first_level = splited_string[4]
                second_level = splited_string[5]
                emp_id = splited_string[6]
                if not Progress.objects.filter(course_name__iexact=course_name, person_email__iexact=employee_email).exists():
                    Progress.objects.filter(course_name__iexact=course_name, person_email__iexact=employee_email).delete()
                    PostScenario.objects.filter(associated_course__iexact=course_name, person_email__iexact=employee_email).delete()
                    QuestionAttempted.objects.filter(course_name__iexact=course_name, person_email__iexact=employee_email).delete()
                    CompletedModuledetail.objects.filter(course_name__iexact=course_name, person_email__iexact=employee_email).delete()
                    if expiration_date == '':
                        obj = Progress.objects.create(course_name=course_name, person_email=employee_email, person_team=team_name,
                                            person_name=employee_name, person_location=location,
                                            person_firstlevel=first_level, person_secondlevel=second_level, person_empid=emp_id)
                    else:
                        obj = Progress.objects.create(course_name=course_name, person_email=employee_email, person_team=team_name,
                                            person_name=employee_name, person_location=location, expiration_date=expiration_date,
                                            person_firstlevel=first_level, person_secondlevel=second_level, person_empid=emp_id)
                    messages.success(request, 'Course assigned successfuly!')
                    #email notification to person to which course is assigned
                    # if trigger_email == "on":
                        # send_mail('Let\'s Learn More', f'Dear {obj.person_name},\n\nHere is an opportunity to enhance your skills and knowledge of the processes.\n\nUse it before you lose it.'
                        #                            f'\n\nTraining Course - {obj.course_name}\nExpiry Date - {obj.expiration_date}\n\nLogin at - https://lms.dfgateway.com\n\nHappy Learning!\n\nRegards,'
                        #                            f'\nTraining Team', 'Study Hall <studyhall@dataflowgroup.com>', [obj.person_email], auth_user='analytics@dataflowgroup.com', fail_silently=False)

                else:
                    messages.warning(request, 'Course already assigned to the user')
        elif category == 'self-assign':
            # self-assigning user email
            self_email = request.user.email 


            # AWS connection
            if socket.gethostbyname(socket.gethostname()) == '10.2.5.128' or socket.gethostbyname(socket.gethostname()) == '10.2.1.230':
                engine = create_engine('postgresql://analytics:analytics@123@ec2-34-246-108-106.eu-west-1.compute.amazonaws.com:5432/iadatabase')
                df_aws = pd.read_sql_query('select * from "headcount_master_darwinbox"', con=engine)
                df = df_aws[['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting', 'Employee Code']]
                df = df.loc[df['Email Id'] == self_email, :]
            else:
                df = pd.DataFrame(columns=['Employee Name', 'Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting',
                                           '2nd Level Reporting', 'Employee Code'])
                df.loc[0] = ['Ankur', 'ankurkalakoti@gmail.com', 'Analytcs', 'Noida', 'Rathore', 'agarwal', '11111']
                df.loc[1] = ['Anubhav', 'anubhav.kumar27@gmail.com', 'Analytcs', 'Noida', 'Rathore', 'agarwal', '11111']
                df.loc[2] = ['Raghav', 'princeroyale72@gmail.com', 'Analytcs', 'Noida', 'Rathore', 'agarwal', '11111']
                df.loc[3] = ['officialAnkur', 'officialankursingh97@gmail.com', 'Analytcs', 'Noida', 'Rathore', 'agarwal', '11111']

                df = df.loc[df['Email Id'] == self_email, :]
            for i, j in df.iterrows():
                if not Progress.objects.filter(course_name=course_name, person_email=j['Email Id']).exists():
                    obj = Progress.objects.create(course_name=course_name, person_email=j['Email Id'], person_team=j['Sub-Department'], person_name=j['Employee Name'], expiration_date=expiration_date, person_location=j['DF Site'], person_firstlevel=j['1st Level Reporting'], person_secondlevel=j['2nd Level Reporting'], person_empid=j['Employee Code'], testgiven_status=False)

            return redirect('employee:employeehome')
        return redirect('adminboard:assign')
    return redirect('adminboard:assign')


@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def delmod(request, modname):
    Module.objects.filter(module_name=modname).update(status='Archived')
    CompletedModuledetail.objects.filter(completed_module__iexact=modname).update(module_status='Archived')
    Question.objects.filter(module_name__iexact=modname).update(flag='Archived')
    Scenario.objects.filter(associated_module__iexact=modname).update(flag='Archived')
    Course.objects.filter(module__module_name__iexact=modname).delete()
    return redirect('adminboard:viewmodule')

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def delcourse(request, cname):
    entry_email = request.user.email
    Course.objects.filter(course_name__iexact=cname).update(course_status='deleted')
    if Progress.objects.filter(course_name=cname).exists():
        obj = Progress.objects.get(course_name=cname)
        obj.course_status = 'deleted'
        obj.save()
    return redirect('adminboard:adminhome')

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
@csrf_exempt
def putexpdate(request, id):
    if request.method == 'POST':
        exp_date = request.POST.get(f'expired_date__{id}')
        obj = Progress.objects.get(pk=id)
        obj.expiration_date = exp_date
        obj.save()
        return HttpResponse('')
    return redirect('adminboard:people')


@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def testrestart(request, id):
    obj = Progress.objects.get(pk=id)
    obj.testgiven_status = False
    obj.test_startflag = False
    obj.save()
    return HttpResponse('')

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def getcasestudy(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    case_study_all = Scenario.objects.filter(flag__iexact='Active')
    return render(request, 'adminboard/viewcase.html', {'case_study_all': case_study_all, 'entry_email': entry_email, 'admin_emails': admin_emails})


@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def getallquest(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    quest_data = []
    all_quest = Question.objects.filter(flag__iexact='Active')
    for i in all_quest:
        quest_attempted = len(QuestionAttempted.objects.filter(quest_id=i.id))
        quest_skipped = len(QuestionAttempted.objects.filter(quest_id=i.id, is_correct__iexact='skipped'))
        quest_corrected = len(QuestionAttempted.objects.filter(quest_id=i.id, is_correct=True))
        try:
            perc_correct = (quest_corrected/quest_attempted) * 100
        except:
            perc_correct = 'Not Attempted'
        that_quest = Question.objects.get(pk=i.id)
        quest_data.append((that_quest.id, that_quest.question, that_quest.option1, that_quest.option2, that_quest.option3, that_quest.option4, that_quest.correct_option, quest_attempted, quest_skipped, perc_correct, that_quest.module_name))
    return render(request, 'adminboard/viewquest.html', {'entry_email': entry_email, 'admin_emails': admin_emails, 'quest_data': quest_data})


@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
@csrf_exempt
def filterpeople(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    if request.method == 'POST':
        datepicker = request.POST.get('datepicker')
        datepicker = datepicker.split(' - ')
        date_from = datepicker[0].split('/')
        date_from = date_from[2] + '-' + date_from[0] + '-' + date_from[1]
        date_to = datepicker[1].split('/')
        date_to = date_to[2] + '-' + date_to[0] + '-' + date_to[1]
        entry_email = request.user.email
        candidates = Progress.objects.filter(expiration_date__range=[date_from, date_to])
        return render(request, 'adminboard/people.html', {'entry_email': entry_email, 'admin_emails': admin_emails, 'candidates': candidates})
    return redirect('adminboard:people')


@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def delprocess_name(request, id):
    Process.objects.get(pk=id).delete()
    return redirect('adminboard:addmodule')

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def addprocess_name(request):
    if request.method == 'POST':
        process_name = request.POST.get('process_name')
        if not Process.objects.filter(process_name__iexact=process_name).exists():
            Process.objects.create(process_name=process_name)
        return HttpResponse('')
    return redirect('adminboard:addmodule')

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def edit_quest(request, id):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    quest = Question.objects.get(pk=id)
    modules = Module.objects.filter(status__iexact='Active')
    return render(request, 'adminboard/finalquest.html', {'quest': quest, 'admin_emails': admin_emails, 'modules': modules,
                                                             'entry_email': request.user.email})

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def edit_scenario(request, id):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    scenario = Scenario.objects.get(pk=id).scenario_desc
    scenario = Scenario.objects.filter(scenario_desc__exact=scenario)[0]
    modules_in_sc = [i.associated_module for i in Scenario.objects.filter(scenario_desc__exact=scenario)]
    modules = Module.objects.filter(status__iexact='Active')
    return render(request, 'adminboard/caseStudy.html', {'scenario': scenario, 'admin_emails': admin_emails,
                                                             'entry_email': request.user.email, 'modules': modules, 'modules_in_sc':modules_in_sc})
@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def revoke(request, id):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    CompletedModuledetail.objects.filter(person_email__exact=Progress.objects.get(pk=id).person_email
                                    , course_name__iexact=Progress.objects.get(pk=id).course_name).delete()

    PostScenario.objects.filter(person_email__exact=Progress.objects.get(pk=id).person_email,
                                        associated_course__iexact=Progress.objects.get(pk=id).course_name).delete()
    Progress.objects.filter(pk=id).delete()
    return HttpResponse('')

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def upload_bulk_quest(request):
    if request.method == 'POST':
        file = request.FILES.get('bulk-upload')
        df = pd.read_csv(file, index_col=None)

        df = df.fillna('NA')
        for i, j in df.iterrows():
            Question.objects.create(module_name=j[0], question=j[1], option1=j[2], option2=j[3],
             option3=j[4], option4=j[5], correct_option=j[6], flag='Active')
        messages.success(request, 'All questions uploaded successfuly!')
        return redirect('adminboard:finalquest')
    return redirect('adminboard:finalquest')

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def editmod(request, mname):
    mod = Module.objects.filter(module_name__exact=mname)[0]
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    process_name = Process.objects.all()
    locations = ['Mumbai', 'Amman', 'Noida', 'Hyderabad', 'Dubai', 'Bangkok',
                 'Singapore City', 'Manila', 'London', 'Cairo', 'Berlin', 'Kochi',
                 'Kuala Lumpur', 'Doha', 'Manama', 'Riyadh']
    modules = Module.objects.values_list('module_name', flat=True).distinct()
    return render(request, 'adminboard/addMod.html',
                  {'modules': modules, 'locations': locations, 'process_name': process_name, 'entry_email': entry_email,
                   'admin_emails': admin_emails, "module": mod})

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def submission(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    contributions = Contribution.objects.all()

    return render(request, 'adminboard/contribution.html', {'entry_email': entry_email, 'admin_emails': admin_emails, 'contributions':contributions})

@csrf_exempt
@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def status(request, id):
    if request.method == 'POST':
        remark = request.POST.get('remark')
        status = request.POST.get('status')
        score = request.POST.get('score')
        obj = Contribution.objects.get(pk=id)
        obj.remark = remark
        obj.status = status
        obj.score = score
        # obj.save()

        # Mail Formatter
        welcome_mail = WelcomeMail()
        to = [obj.contributor_email]
        from_email = 'Study Hall <studyhall@dataflowgroup.com>'
        if status == "Rejected":
            subject = "CONTRIBUTION REJECTED"
            title = "Thank you for your contribution!"
            content = "We truly appreciate your effort to contribute content to the Study Hall. We will be keeping this article for now and will notify you once a relevant topic is published.\n\n Please continue to send in your articles and we look forward to hearing from you again very soon!"
            button_label = ""
            button_link = ""
        else:
            subject = "CONTRIBUTION ACCEPTED"
            title = "Congratulations!"
            content = "Your case study/essential training content has just been added to the Study Hall! You will receive an email containing your e-voucher shortly!\n\n Thank you and look forward to more contributions from you soon!"
            button_label = ""
            button_link = ""

        welcome_mail.set_context(subject, title, content, button_label, button_link)
        welcome_mail.send(to, from_email=from_email, bcc=[], connection=None, attachments=[],
                   headers={}, cc=[], reply_to=[], fail_silently=False)

        return HttpResponse('')
    return HttpResponse('')

from adminboard.models import Carousel
from adminboard.models import MinMaxCarousel
@csrf_exempt
@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def configuration(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    courses = Course.objects.values_list('course_name', flat=True).distinct()
    if request.method == 'POST':
        carousel_type = request.POST.get('carousel_type')
        carousel_title = request.POST.get('carousel_title')
        carousel_description = request.POST.get('carousel_description')
        carousel_course = request.POST.get('carousel_course')
        carousel_link = request.POST.get('carousel_link')
        carousel_cover = request.FILES.get('carousel_cover')

        Carousel.objects.create(carousel_type=carousel_type, carousel_title=carousel_title, carousel_description=carousel_description, carousel_course=carousel_course, carousel_cover=carousel_cover, carousel_link=carousel_link)
        messages.success(request, 'Carousel details saved successfully!')
        return redirect('adminboard:configuration')
    return render(request, 'adminboard/configuration.html', {'entry_email':entry_email ,'admin_emails': admin_emails, 'courses':courses, 'carousels': Carousel.objects.all(), 'minmax': MinMaxCarousel.objects.all().last()})


@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def delCarousel(request, id):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    Carousel.objects.filter(pk=id).delete()
    return redirect('adminboard:configuration')

@csrf_exempt
@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def minMax(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    if request.method == 'POST':
        id = request.POST.get('id')
        min = request.POST.get('min')
        max = request.POST.get('max')
        obj, created = MinMaxCarousel.objects.update_or_create(pk=id, defaults={"min":min, "max":max})
    return redirect('adminboard:configuration')


@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def userassessment(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    contributions = list(QuestionAttempted.objects.all().values('id', 'person_email', 'course_name', 'quest_id', 'option_given', 'is_correct'))

    for quest_submitted in contributions:
        quest_id = quest_submitted['quest_id']
        quest_obj = Question.objects.get(pk=quest_id)
        quest_submitted['module_linked'] = quest_obj.module_name
        quest_submitted['question'] = quest_obj.question
        quest_submitted['option1'] = quest_obj.option1
        quest_submitted['option2'] = quest_obj.option2
        quest_submitted['option3'] = quest_obj.option3
        quest_submitted['option4'] = quest_obj.option4        

    return render(request, 'adminboard/userassessment.html', {'entry_email': entry_email, 'admin_emails': admin_emails, 'contributions':contributions})


@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def questions(request):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    quest_answer = QnA.objects.all().order_by('-created_date')
    if request.method == 'POST':
        question = request.POST.get('question')
        rejected_remark = request.POST.get('rejected_remark')
        status = request.POST.get('status')
        answer = request.POST.get('answer')
        obj = QnA.objects.get(pk=request.POST.get('id'))
        obj.status = status
        obj.question = question
        obj.answer = answer
        obj.rejected_remark = rejected_remark
        obj.closed_date = datetime.now() if status != 'Pending' else None
        obj.save()

        if status == 'Rejected':
            pass
            # # Mail Formatter
            # welcome_mail = WelcomeMail()
            # from_email = 'analytics@dataflowgroup.com'
            # subject = f"Update on your query on studyhall"
            # title = f"You have message on module: {obj.module_name}"
            # content = f"We’ve just replied to your query in the module{obj.module_name}: {obj.question} today.\n\nClick the button below to see the reply!\n\nHappy Learning! {obj.answer} \n\nHere is : {obj.answer}"
            # # button_label = "Studyhall"
            # # button_link = f"https://uatcab.dfgateway.com/"
            # welcome_mail.set_context(subject, title, content, button_label, button_link)
            # welcome_mail.send([obj.progress.person_email], from_email=from_email, bcc=[], connection=None, attachments=[], headers={}, cc=[], reply_to=[], fail_silently=False)
        else:
            pass
            # # Mail Formatter
            # welcome_mail = WelcomeMail()
            # from_email = 'analytics@dataflowgroup.com'
            # subject = f"Update on your query on studyhall"
            # title = f"You have message on module: {obj.module_name}"
            # content = f"We’ve just replied to your query in the module{obj.module_name}: {obj.question} today.\n\nClick the button below to see the reply!\n\nHappy Learning! {obj.answer} \n\nHere is : {obj.answer}"
            # # button_label = "Studyhall"
            # # button_link = f"https://uatcab.dfgateway.com/"
            # welcome_mail.set_context(subject, title, content, button_label, button_link)
            # welcome_mail.send([obj.progress.person_email], from_email=from_email, bcc=[], connection=None, attachments=[], headers={}, cc=[], reply_to=[], fail_silently=False)
        
        return redirect('adminboard:questions')
    return render(request, 'adminboard/questions.html', {'entry_email': entry_email, 'admin_emails': admin_emails, 'quest_answer': quest_answer})

@user_passes_test(authentication_check, login_url='/adminboard/', redirect_field_name=None)
def questionsForm(request, id):
    admin_emails = [i.admin_email for i in AuthorizedPanel.objects.all()]
    entry_email = request.user.email
    quest_answer = QnA.objects.get(pk=id)
    return render(request, 'adminboard/questionForm.html', {'id': id, 'quest_answer': quest_answer, 'entry_email': entry_email, 'admin_emails': admin_emails})
