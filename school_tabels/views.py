from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (CreateView, UpdateView, DeleteView, FormView)
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers

from .mixins import LastUpdaterMixin
from .forms import (AddClassForm, AddExamTabelForm,
                    AddFullScheduleForm, AddFullScheduleModelForm,
                    ChooseExamInfoForm, AddClassRoomForm,
                    AddSubjectForm, ScheduleSearchForm, ExamsTabelSearchForm)

from .formsets import (schedule_formset, EditScheduleFormset,
                       exam_formset
                       )
from .models import (Exam, ExamTabel, TheClass, Article,
                     SchoolSchedule, ClassRoom)
from students import models


class AddSubjectView(CreateView):
    form_class = AddSubjectForm
    template_name = 'tabels/add_subject.html'
    success_url = reverse_lazy('main:subjects-dashboard')


class EditSubjectView(UpdateView):
    queryset = Article.objects.all()
    form_class = AddSubjectForm
    template_name = 'tabels/add_subject.html'
    success_url = reverse_lazy('main:subjects-dashboard')


class DeleteSubjectView(DeleteView):
    queryset = Article.objects.all()

    template_name = 'tabels/delete_subject_confirm.html'
    success_url = reverse_lazy('main:subjects-dashboard')


class AddClassView(CreateView):
    form_class = AddClassForm
    template_name = 'tabels/add_class.html'
    success_url = reverse_lazy('main:classes-dashboard')


class EditClassView(UpdateView):
    queryset = TheClass.objects.all()
    form_class = AddClassForm
    template_name = 'tabels/add_class.html'
    success_url = reverse_lazy('main:classes-dashboard')


class DeleteClassView(DeleteView):
    queryset = TheClass.objects.all()
    template_name = 'tabels/delete_class_confirm.html'
    success_url = reverse_lazy('main:classes-dashboard')


class AddClassRoomView(CreateView):
    form_class = AddClassRoomForm
    template_name = 'tabels/add_classroom.html'
    success_url = reverse_lazy('main:classrooms-dashboard')


class EditClassRoomView(UpdateView):
    queryset = ClassRoom.objects.all()
    form_class = AddClassRoomForm
    template_name = 'tabels/add_classroom.html'
    success_url = reverse_lazy('main:classrooms-dashboard')


class DeleteClassroomView(DeleteView):
    queryset = ClassRoom.objects.all()
    template_name = 'tabels/delete_classroom_confirm.html'
    success_url = reverse_lazy('main:classrooms-dashboard')


def add_edit_exam_tabel_view(request, pk=None):
    extra = 10
    instance = None
    delete = False
    queryset = Exam.objects.none()
    if pk != None:
        delete = True
        instance = get_object_or_404(ExamTabel, pk=pk)
        queryset = instance.exams.all()
        extra = 0
    form = AddExamTabelForm(request.POST or None, instance=instance)
    formset = exam_formset(delete, extra)(request.POST or None,
                                          queryset=queryset)
    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            obj = form.save()
            for fm in formset:
                date = fm.cleaned_data.get('the_date')
                article = fm.cleaned_data.get('article')
                if date and article:
                    exam_obj = fm.save(commit=False)
                    exam_obj.exam_tabel = obj
                    exam_obj.save()
            return redirect('main:exams-dashboard')
    context = {'form': form, 'formset': formset}
    return render(request, 'tabels/add_exams_tabel.html', context)


class DeleteExamTabelView(DeleteView):
    queryset = ExamTabel.objects.all()
    template_name = 'tabels/delete_exams_tabel_confirm.html'
    success_url = reverse_lazy('main:exams-dashboard')


HUMAN_COUNT = {'1': 'يوم واحد', '2': 'يومان', '3': 'ثلاث أيام',
               '4': 'أربع أيام', '5': 'خمس أيام'}


def add_edit_full_schedule_view(request, class_id=''):
    data = {}
    extra = 5
    qs = SchoolSchedule.objects.none()
    if class_id:
        class_ = get_object_or_404(ClassRoom, id=class_id)
        data['class_room'] = class_
        qs = SchoolSchedule.objects.filter(
            class_room__id=class_id).order_by('day')
        extra = 0
    classroom_form = AddFullScheduleForm(request.POST or None, initial=data)

    formset = schedule_formset(True, extra=extra)(request.POST or None,
                                                  queryset=qs)
    if request.method == 'POST':
        if classroom_form.is_valid() and formset.is_valid():
            class_room = classroom_form.cleaned_data.get('class_room')
            for form in formset:
                if form.is_valid():
                    day = form.cleaned_data.get('day')
                    if day:
                        obj = form.save(commit=False)
                        obj.class_room = class_room
                        obj.save()
            msg = 'تم إضافة جدول حصص جديد'
            messages.add_message(request, messages.INFO, msg)
            return redirect('main:classes-tabel-dashboard')
    context = {'formset': formset, 'classroom_form': classroom_form}
    return render(request, 'tabels/add_full_schedule.html', context)


def delete_full_schedule_view(request, class_id):
    class_ = get_object_or_404(ClassRoom, id=class_id)
    days_schedule = class_.days.all()
    if request.method == 'POST':
        days_schedule.delete()
        url = reverse('main:classes-tabel-dashboard')
        return redirect(url + '#schedules-id')
    context = {'object': class_}
    return render(request, 'tabels/delete_full_schedule.html', context)


class ScheduleDetailView(FormView):
    form_class = ScheduleSearchForm
    template_name = 'tabels/schedule_search.html'
    success_url = reverse_lazy('tabels:schedule-detail')


class ExamsTabelDetailView(FormView):
    form_class = ExamsTabelSearchForm
    template_name = 'tabels/exams_tabel_search.html'
    success_url = reverse_lazy('tabels:exams-tabel-detail')
