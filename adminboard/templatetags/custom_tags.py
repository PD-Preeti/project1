from django import template
from adminboard.models import Course
from datetime import datetime, timedelta, date

register = template.Library()

@register.simple_tag
def badge_giver(course_name):
    created_time = Course.objects.filter(course_name__iexact=course_name)[0].created_time
    updated_time = Course.objects.filter(course_name__iexact=course_name)[0].updated_time
    todays_date = datetime.today() + timedelta(hours=5.5)
    if created_time == updated_time:
        return False
    else:
        todays_date = todays_date.strftime('%Y/%m/%d').split('/')
        updated_time = updated_time.strftime('%Y/%m/%d').split('/')

        todays_date = date(int(todays_date[0]), int(todays_date[1]), int(todays_date[2]))
        updated_time = date(int(updated_time[0]), int(updated_time[1]), int(updated_time[2]))
        delta = updated_time - todays_date
        days = delta.days
        if days < 7:
            return True
        else:
            return False

@register.filter(name='split')
def split(value, key):
    return value.split(key)