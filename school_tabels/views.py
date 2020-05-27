from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import (CreateView, UpdateView, DeleteView, FormView)
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _

from .mixins import DeleteSuccessMessageMixin
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


class AddSubjectView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = AddSubjectForm
    template_name = 'tabels/add_subject.html'
    success_url = reverse_lazy('main:subjects-dashboard')
    success_message = _('A new subject has been added')


class EditSubjectView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    queryset = Article.objects.all()
    form_class = AddSubjectForm
    template_name = 'tabels/add_subject.html'
    success_url = reverse_lazy('main:subjects-dashboard')
    success_message = _('The Subject has been modified')


class DeleteSubjectView(LoginRequiredMixin, DeleteSuccessMessageMixin, DeleteView):
    queryset = Article.objects.all()
    template_name = 'tabels/delete_subject_confirm.html'
    success_url = reverse_lazy('main:subjects-dashboard')
    success_message = _('The Subject has been Deleted')


class AddClassView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = AddClassForm
    template_name = 'tabels/add_class.html'
    success_url = reverse_lazy('main:classes-dashboard')
    success_message = _('A new class has been added')


class EditClassView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    queryset = TheClass.objects.all()
    form_class = AddClassForm
    template_name = 'tabels/add_class.html'
    success_url = reverse_lazy('main:classes-dashboard')
    success_message = _('The class has been modified')


class DeleteClassView(LoginRequiredMixin, DeleteSuccessMessageMixin, DeleteView):
    queryset = TheClass.objects.all()
    template_name = 'tabels/delete_class_confirm.html'
    success_url = reverse_lazy('main:classes-dashboard')
    success_message = _('The class has been deleted')


class AddClassRoomView(LoginRequiredMixin, SuccessMessageMixin,CreateView):
    form_class = AddClassRoomForm
    template_name = 'tabels/add_classroom.html'
    success_url = reverse_lazy('main:classrooms-dashboard')
    success_message = _('A new classroom has been added')

class EditClassRoomView(LoginRequiredMixin, SuccessMessageMixin,UpdateView):
    queryset = ClassRoom.objects.all()
    form_class = AddClassRoomForm
    template_name = 'tabels/add_classroom.html'
    success_url = reverse_lazy('main:classrooms-dashboard')
    success_message = _('The classroom has been modified')


class DeleteClassroomView(LoginRequiredMixin, DeleteSuccessMessageMixin,DeleteView):
    queryset = ClassRoom.objects.all()
    template_name = 'tabels/delete_classroom_confirm.html'
    success_url = reverse_lazy('main:classrooms-dashboard')
    success_message = _('The classroom has been deleted')

@login_required
def add_edit_exam_tabel_view(request, pk=None):
    extra = 2
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
            obj = form.save(commit=False)
            obj.last_editor = request.user.username
            obj.save()
            for fm in formset:
                date = fm.cleaned_data.get('the_date')
                article = fm.cleaned_data.get('subject')
                if date and article:
                    exam_obj = fm.save(commit=False)
                    exam_obj.exam_tabel = obj
                    exam_obj.save()
            msg = _('A new exams schedule has been added')
            if instance:
                msg = _('Exams schedule has been modified')
            messages.add_message(request, messages.SUCCESS, msg)
            return redirect('main:exams-dashboard')
    context = {'form': form, 'formset': formset, 'object': instance}
    return render(request, 'tabels/add_exams_tabel.html', context)


class DeleteExamTabelView(LoginRequiredMixin, DeleteSuccessMessageMixin, DeleteView):
    queryset = ExamTabel.objects.all()
    template_name = 'tabels/delete_exams_tabel_confirm.html'
    success_url = reverse_lazy('main:exams-dashboard')
    success_message = _('Exams schedule has been deleted')


HUMAN_COUNT = {'1': 'يوم واحد', '2': 'يومان', '3': 'ثلاث أيام',
               '4': 'أربع أيام', '5': 'خمس أيام'}


@login_required
def add_edit_full_schedule_view(request, class_id=''):
    data = {}
    extra = 1
    classroom = None
    qs = SchoolSchedule.objects.none()
    if class_id:
        classroom = get_object_or_404(ClassRoom, id=class_id)
        data['class_room'] = classroom
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
            msg = _('A new classes schedule has been added')
            if classroom:
                msg = _('The classes schedule has been modified')
            messages.add_message(request, messages.INFO, msg)
            return redirect('main:classes-tabel-dashboard')

    context = {'formset': formset,
               'classroom_form': classroom_form,
               'object': classroom}
    return render(request, 'tabels/add_full_schedule.html', context)


@login_required
def delete_full_schedule_view(request, class_id):
    classroom = get_object_or_404(ClassRoom, id=class_id)
    days_schedule = classroom.days.all()
    if request.method == 'POST':
        days_schedule.delete()
        url = reverse('main:classes-tabel-dashboard')
        return redirect(url + '#schedules-id')
    context = {'classroom_name': classroom.name}
    return render(request, 'tabels/delete_full_schedule.html', context)


class ScheduleDetailView(FormView):
    form_class = ScheduleSearchForm
    template_name = 'tabels/schedule_search.html'
    success_url = reverse_lazy('tabels:schedule-detail')


class ExamsTabelDetailView(FormView):
    form_class = ExamsTabelSearchForm
    template_name = 'tabels/exams_tabel_search.html'
    success_url = reverse_lazy('tabels:exams-tabel-detail')
