from django import template

register = template.Library()


@register.filter(name="arabic_gender")
def get_gender_name(word):
    our_dic = {'ml': 'ذكر',
               'fl': 'أنثى'}
    return our_dic.get(word)


@register.filter(name="human_counter")
def get_human_counter(word):
    our_dic = {'0': 'الترتيب صفر', '1': 'الأول', '2': 'الثاني', '3': 'الثالث',
               '4': 'الرابع', '5': 'الخامس', '6': 'السادس',
               '7': 'السابع', '8': 'الثامن', '9': 'التاسع',
               '10': 'العاشر', '11': 'الحادي عشر', '12': 'الثاني عشر',
               '13': 'الثالث عشر', '14': 'الرابع عشر', '15': 'الخامس عشر',
               '16': 'السادس عشر', '17': 'السابع عشر', '18': 'الثامن عشر',
               '19': 'التاسع عشر', '20': 'العشرون', '21': 'الحادي و العشرون', }
    return our_dic.get(str(word), str(word))


@register.filter(name="semester_counter")
def get_semester_counter(word):
    our_dic = {'1': 'الأولى',
               '2': 'الثانية',
               '3': 'الثالثة'}
    return our_dic.get(str(word), str(word))
