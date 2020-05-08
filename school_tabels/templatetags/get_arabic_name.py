from django import template

register = template.Library()


@register.filter(name='class_name')
def get_class_name(text):
    our_dic = {'1': 'الأول', '2': 'الثاني', '3': 'الثالث', '4': 'الرابع',
               '5': 'الخامس', '6': 'السادس', '7': 'السابع', '8': 'الثامن',
               '9': 'التاسع', }
    return our_dic.get(text)


@register.filter(name='arabic_weekday')
def get_weekday_name(text):
    our_dic = {'sunday': 'الأحد', 'monday': 'الإثنين', 'tuesday': 'الثلاثاء', 'wednesday': 'الأربعاء',
               'tursday': 'الخميس', 'saturday': 'السبت'}
    return our_dic.get(text)


@register.filter(name='semester')
def get_arabic_season_name(text):

    semesters = {'1': 'الأولى', '2': 'الثانية',
                 '3': 'الثالثة'}

    return semesters.get(text)


@register.filter(name='human_exam_type')
def human_exam_type(text):

    types = {'1': 'نصفي', '2': 'نهائي'}

    return types.get(text)
