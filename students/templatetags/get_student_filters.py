from django import template


register = template.Library()


@register.filter(name="lang_gender")
def get_gender_name(word, lang):
    ar_dic = {'ml': 'ذكر',
              'fl': 'أنثى'}
    en_dic = {'ml': 'mail',
              'fl': 'femail'}
    result = ar_dic.get(word)
    if lang == 'en':
        result = en_dic.get(word)
    return result
