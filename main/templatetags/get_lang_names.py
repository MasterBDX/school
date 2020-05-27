from django import template
from main.vars import (SEMESTERS_DIC, TYPE_DIC, HUMAN_COUNTER_DIC,GENDER_DIC)

register = template.Library()


@register.filter(name='class_name')
def get_class_name(text):
    our_dic = {'1': 'الأول', '2': 'الثاني', '3': 'الثالث', '4': 'الرابع',
               '5': 'الخامس', '6': 'السادس', '7': 'السابع', '8': 'الثامن',
               '9': 'التاسع', }
    return our_dic.get(text)


@register.filter(name='semester')
def get_arabic_season_name(value, lang):
    name = SEMESTERS_DIC.get(value).get(lang)
    return name


@register.filter(name='type')
def human_exam_type(value, lang):
    type_ = TYPE_DIC.get(value).get(lang)
    return type_


@register.filter(name="human_counter")
def get_human_counter(word):
    return HUMAN_COUNTER_DIC.get(str(word), str(word))

@register.filter(name="lang_gender")
def get_right_gender_name(value):
    return GENDER_DIC.get(value)