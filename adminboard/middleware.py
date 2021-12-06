from datetime import datetime, timedelta
from employee.models import Progress
from django.utils.deprecation import MiddlewareMixin
from adminboard.mails import WelcomeMail
import socket
from django.db.models import Max
from adminboard.models import DailyCheck
from adminboard.models import Course, Question


#class CustomMiddleware:
#    def __init__(self, get_response):
#        self.get_response = get_response

#    def __call__(self, request):
#        response = self.get_response(request)
#        response["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
#        response["Pragma"] = "no-cache" # HTTP 1.0.
#        response["Expires"] = "0" # Proxies.
#        return response

#class MailerMiddleware(MiddlewareMixin):
#    def process_request(self, request):
#        all_users = Progress.objects.filter(testgiven_status=False)
        # check questions
#        courses_assgined = [i.course_name for i in Progress.objects.filter(testgiven_status=False).exclude(course_status__iexact='deleted')]
#        course_and_quest = []
#        for i in courses_assgined:
#            modules_in_c = [j.module.module_name for j in Course.objects.filter(course_name__iexact=i)]
#            quest_count = Question.objects.filter(module_name__in=modules_in_c).count()
#            course_and_quest.append((i, quest_count))

#        for i in all_users:
#            quest_count_final = 0
#            for a, b in course_and_quest:
#                if i.course_name == a:
#                    quest_count_final += b

#            if quest_count_final > 0:
#                couse_assigndate = i.couse_assigndate
#                if (datetime.today().date() - i.couse_assigndate.date()) > timedelta(days=30) and datetime.now().date().day == 10:
#                    if socket.gethostbyname(socket.gethostname()) == '10.2.5.128':
#                        # # Mail Formatter
#                        welcome_mail = WelcomeMail()
#                        from_email = 'Study Hall <studuyhall@dataflowgroup.com>'
#                        subject = "Course is pending for 30 days"
#                        title = "Do You Need Help?"
#                        content = f"We see that {i.course_name} course has been in progress for more than 30 days already - do you need help? \n \n If you do - just reach out to us on: studyhall@dataflowgroup.com and we will be right with you!"
#                        button_label = ""
#                        button_link = f""
#                        to = [i.person_email]
#                        welcome_mail.set_context(subject, title, content, button_label, button_link)
#                        welcome_mail.send(to, from_email=from_email, bcc=[], connection=None, attachments=[], headers={}, cc=[], reply_to=[], fail_silently=False)
#                    else:
#                        break
#            else:
#                continue


#class MailerTwoMiddleware(MiddlewareMixin):
#    def process_request(self, request):
#        all_users = Progress.objects.values('person_email').annotate(max_id=Max('id'))
#        for i in all_users:
#            obj = Progress.objects.get(pk=i['max_id'])
#            if (datetime.today().date() - obj.couse_assigndate.date()) > timedelta(days=30) and datetime.now().date().day == 10:
#                if socket.gethostbyname(socket.gethostname()) == '10.2.5.128':
#                    # # Mail Formatter
#                    welcome_mail = WelcomeMail()
#                    from_email = 'Study Hall <studuyhall@dataflowgroup.com>'
#                    subject = "No course taken for the past 30 days"
#                    title = "Hey There!"
#                    content = f"It’s been a while since we last saw you and we’ve added courses and modules which you may be interested in.\n\nClick the button below to see what we’ve just added!"
#                    button_label = "Click Here"
#                    button_link = f"https://studyhall.dfgateway.com/"
#                    to = i['person_email']
#                    welcome_mail.set_context(subject, title, content, button_label, button_link)
#                    welcome_mail.send([to], from_email=from_email, bcc=[], connection=None, attachments=[], headers={}, cc=[], reply_to=[], fail_silently=False)
#                else:
#                    break
#        

        


        # # Mail Formatter
        # welcome_mail = WelcomeMail()
        # from_email = 'Study Hall <studyhall@dataflowgroup.com>'
        # subject = "New Course is up"
        # title = "Are you ready to LEARN something new?"
        # content = f"We’ve just uploaded the course/module {course_name} today.\n\nClick the register button below to save a seat!\n\nHappy Learning!"
        # button_label = ""
        # button_link = f""
