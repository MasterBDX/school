from django.forms import modelformset_factory, formset_factory
from .forms import (AddSubjectResultForm, SelectSubjectForm,
                    AddClassGradesForm, AddCompensatoryExamForm,
                    EditCompensatoryExamForm)
from .models import SubjectResult, ClassGrade, CompensatoryExam


subjects_results_formset = modelformset_factory(
    SubjectResult, form=AddSubjectResultForm,
    extra=0)

edit_class_grades_formset = modelformset_factory(
    ClassGrade, form=AddClassGradesForm, extra=0
)

com_exams_formset = modelformset_factory(
    CompensatoryExam,
    form=AddCompensatoryExamForm,
    extra=1)


edit_com_exams_formset = modelformset_factory(
    CompensatoryExam,
    form=EditCompensatoryExamForm,
    extra=0)
