from django import template
from school_tabels.vars import MONTHS

register = template.Library()


@register.filter(name='ar_date')
def get_ar_date(value):
    date = value.strftime(' %-d / %Y - %-I:%M ')
    pm_am = value.strftime('%p')
    if pm_am == 'PM':
        pm_am = 'مساء'

    else:
        pm_am = 'صباحا'
    month = MONTHS.get(value.month)
    return month + ' / ' + date + ' ' + pm_am
