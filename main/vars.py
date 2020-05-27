from django.utils.translation import pgettext_lazy, ugettext_lazy as _
from datetime import datetime

STUDENTS_CLASSES = [('1', 'الأول'), ('2', 'الثاني'),
                    ('3', 'الثالث'), ('4', 'الرابع'),
                    ('5', 'الخامس'), ('6', 'السادس'),
                    ('7', 'السابع'), ('8', 'الثامن'),
                    ('9', 'التاسع')
                    ]


SEMESTER = [('2', 'الثانية'),
            ('3', 'الثالثة')]

PART = [('2', 'الثاني'),
        ('3', 'الثالث')]


GENDER = [('ml', _('Male')), ('fl', _('Female'))]
GENDER_DIC = {'ml': _('Male'),'fl': _('Female')}

STUDENTS_CLASSES = [('1', 'الأول'), ('2', 'الثاني'),
                    ('3', 'الثالث'), ('4', 'الرابع'),
                    ('5', 'الخامس'), ('6', 'السادس'),
                    ('7', 'السابع'), ('8', 'الثامن'),
                    ('9', 'التاسع')
                    ]

SEMESTERS = [
    ('1', _('First')),
    ('2', _('Second')),
    ('3', _('Third')),
]
SEMESTERS_DIC = {
                 '1': _('First'),
                 '2': _('Second'),
                 '3': _('Third')
                 }

WEEK_DAYS = [('sunday', 'الأحد'), ('monday', 'الإثنين'),
             ('tuesday', 'الثلاثاء'), ('wednesday', 'الأربعاء'),
             ('thursday', 'الخميس')]

# This for Choice Field in exam tabel search
YEARS = [(str(x), str(x)) for x in range(2000, 2035)]

# This for Add Exam Form
YEARS_ = [x for x in reversed(range(2000, 2035))]

# This for Add student Field
BIRTH_YEARS = [x for x in range(1990, datetime.now().year)]


MONTHS = {1: _('January'), 2: _('February'),
          3: _('March'), 4: _('April'),
          5: _('May'), 6: _('June'),
          7: _('July'), 8: _('August '),
          9: _('September'), 10: _('October '),
          11: _('November'), 12: _('December'), }

TYPE = [('1', _('Midterm')), ('2', _('Final')),
        ('3', _('Second Round')), ('4', _('Third Round'))]


TYPE_DIC = {'1': {'ar': 'نصفية', 'en': 'Midterm'},
            '2': {'ar': 'نهائية', 'en': 'Final'},
            '3': {'ar': 'دور ثاني', 'en': 'Second Round'},
            '4': {'ar': 'دور ثالث', 'en': 'Third Round'}}


HUMAN_COUNTER_DIC = {
    '0': _('Zero'), '1': pgettext_lazy('Appearance Order', 'First'), '2': pgettext_lazy('Appearance Order', 'Second'),
    '3': pgettext_lazy('Appearance Order', 'Third'), '4': pgettext_lazy('Appearance Order', 'Fourth'), '5': pgettext_lazy('Appearance Order', 'Fifth'),
    '6': pgettext_lazy('Appearance Order', 'Sixth'), '7': pgettext_lazy('Appearance Order', 'Seventh'), '8': _('Eighth'),
    '9': _('Ninth'), '10': _('Tenth'), '11': _('Eleventh'),
    '12': _('Twelfth'), '13': _('Thirteenth'), '14': _('Fourteenth'),
    '15': _('Fifteenth'), '16': _('Sixteenth'), '17': _('Seventeenth'),
    '18': _('Eighteenth'), '19': _('Nineteenth'), '20': _('Twentieth'),
    '21': _('Twenty-first'), '22': _('Twenty-second'), '23': _('Twenty-third'),
    '24': _('Twenty-fourth'), '25': _('Twenty-fifth')
}

ORDER = [('1', 'الأول'), ('2', 'الثاني'), ('3', 'الثالث')]

ENTRY = [('نظامي', 'نظامي'), ('منتسب', 'منتسب')]
STATUS = [('مستجد', 'مستجد'), ('معيد', 'معيد')]


NATIONALITY = [('Libyan', _('Libyan')),
               ('Egyptian', _('Egyptian')),
               ('Tunisian', _('Tunisian')),
               ('Algerian', _('Algerian')),
               ('Moroccan', _('Moroccan')),
               ('Somali', _('Somali')),
               ('Sudanese', _('Sudanese')),
               ('Syrian', _('Syrian')),
               ('Qatari', _('Qatari')),
               ('Iraqi', _('Iraqi')),
               ('Palestinian', _('Palestinian')),
               ('Jordanian', _('Jordanian')),
               ('Saudi', _('Saudi')),
               ('Nigerian', _('Nigerian')),
               ('Turkish', _('Turkish')),
               ('Lebanese', _('Lebanese')),
               ('Mauritanian', _('Mauritanian')),
               ('Emirati', _('Emirati')), ]

