from django.forms import modelformset_factory, formset_factory

from .forms import AddFullScheduleModelForm, AddExamForm
from .models import SchoolSchedule, Exam


def schedule_formset(delete, extra=0):
    ScheduleFormset = modelformset_factory(SchoolSchedule,
                                           form=AddFullScheduleModelForm,
                                           extra=extra,
                                           can_delete=delete
                                           )
    return ScheduleFormset



def exam_formset(delete, extra=0):
    AddExamsTabelFormset = modelformset_factory(Exam,
                                                form=AddExamForm,
                                                extra=extra,
                                                can_delete=delete)
    return AddExamsTabelFormset
