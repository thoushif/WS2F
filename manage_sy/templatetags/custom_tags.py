from django import template
register = template.Library()
import datetime, pytz
from django.conf import settings

 
@register.filter
def filter_active(queryset, active):
    if active is None:
        active=True
    return queryset.filter(active=active).count()

 
@register.filter
def filter_response(queryset, response):
    count = 0
    if queryset is not None and type(queryset) is not str:
        total = queryset.exclude(response_type=None).count()
        if total == 0:
            total = 1
        count = (queryset.filter(response_type=response).count()/total)*100
    return count


@register.simple_tag
def time_of_day(nickname):
    cur_time = datetime.datetime.now(tz=pytz.timezone(str(settings.TIME_ZONE)))
    
    if cur_time.hour < 12:
        greeting = 'Good Morning '
    elif 12 <= cur_time.hour < 18:
        greeting = 'Good Afternoon '
    else:
        greeting = 'Good Evening '
    return greeting + nickname + "!"