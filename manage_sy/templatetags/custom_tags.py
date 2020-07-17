from django import template
register = template.Library()
import datetime, pytz
from django.conf import settings

@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)

@register.filter
def filter_active(queryset, active):
    return queryset.filter(active=active)

@register.simple_tag
def time_of_day():
    cur_time = datetime.datetime.now(tz=pytz.timezone(str(settings.TIME_ZONE)))
    if cur_time.hour < 12:
        return 'Good Morning!'
    elif 12 <= cur_time.hour < 18:
        return 'Good Afternoon!'
    else:
        return 'Good Evening!'