from django.forms import modelformset_factory, formset_factory
from .forms import (AddSubjectResultForm, SelectSubjectForm,
                    AddCompensatoryExamForm,
                    EditCompensatoryExamForm)
from .models import SubjectResult, ClassGrade, CompensatoryExam


subjects_results_formset = lambda form : modelformset_factory(
    SubjectResult, form=form,
    extra=0)

edit_class_grades_formset = lambda form : modelformset_factory(
    ClassGrade, form=form, extra=0
)

com_exams_formset = modelformset_factory(
    CompensatoryExam,
    form=AddCompensatoryExamForm,
    extra=1,
    can_delete=True)


edit_com_exams_formset = modelformset_factory(
    CompensatoryExam,
    form=EditCompensatoryExamForm,
    extra=0)
