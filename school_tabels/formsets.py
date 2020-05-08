from django.forms import modelformset_factory, formset_factory

from .forms import AddFullScheduleModelForm, AddExamForm
from .models import SchoolSchedule, Exam


def schedule_formset(delete, extra=0):
    ScheduleFormset = modelformset_factory(SchoolSchedule,
                                           form=AddFullScheduleModelForm,
                                           extra=extra,
                                           )
    return ScheduleFormset


EditScheduleFormset = modelformset_factory(SchoolSchedule,
                                           form=AddFullScheduleModelForm,
                                           max_num=5,
                                           extra=0
                                           )


def exam_formset(delete, extra=0):
    AddExamsTabelFormset = modelformset_factory(Exam,
                                                form=AddExamForm,
                                                extra=extra,
                                                can_delete=delete)
    return AddExamsTabelFormset
