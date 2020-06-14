from django.shortcuts import (render, get_object_or_404, redirect, Http404)
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .filters import get_stds_filters
from .models import Student, ResultsPaper
from school_tables.models import ClassRoom

from .forms import (AddStudent, AddResultsPaperForm,
                    AddCompensatoryExamForm,AddClassGradesForm,
                    AddClassGradesSemester3Form,AddSubjectResultForm,
                    AddSubjectResultSemester3Form)

from school_tables.models import TheClass
from .models import (Student, Semester, SubjectResult,
                     ClassGrade, CompensatoryExam)

from .formsets import (subjects_results_formset,
                       edit_class_grades_formset,
                       com_exams_formset)
from main.vars import SEMESTERS_DIC,PART_DIC,HUMAN_COUNTER_DIC
from main.mixins import DeleteSuccessMessageMixin,StudentSuccessUrlMixin


class StudentDetail(LoginRequiredMixin,DetailView):
    queryset = Student.objects.select_related('the_class','classroom')
    template_name = 'students/detail.html'


class StudentPrintableDetail(LoginRequiredMixin,DetailView):
    model = Student
    template_name = 'students/printable_detail.html'
    


class AddStudentView(LoginRequiredMixin,SuccessMessageMixin,StudentSuccessUrlMixin,CreateView):
    form_class = AddStudent
    template_name = "students/add_student.html"
    success_message = _('A new student has been added')
    
    
class EditStudentView(LoginRequiredMixin,SuccessMessageMixin,StudentSuccessUrlMixin,UpdateView):
    context_object_name = 'student'
    queryset = Student.objects.all()
    form_class = AddStudent
    template_name = "students/add_student.html"
    
    success_message = _('The student information has been modified')


class DeleteStudentView(LoginRequiredMixin,DeleteSuccessMessageMixin,StudentSuccessUrlMixin,DeleteView):
    queryset = Student.objects.all()
    template_name = "students/delete_student_confirm.html"
    success_url = reverse_lazy("main:students-classrooms-dashboard")
    success_message = _('The student has been deleted')

class SearchStudentsView(ListView):
    context_object_name = 'students'
    template_name = 'students/search_students.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        q = request.GET.get('q')
        if not q or q.isspace():
            qs = Student.objects.none()
        else:
            qs = Student.objects.select_related('the_class','classroom').filter(get_stds_filters(q))
        return qs


class AddResultsPaperView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    form_class = AddResultsPaperForm
    template_name = 'students/add_results_paper.html'
    success_message = _('A new result paper has been added')

    def get_success_url(self, *args, **kwargs):
        return self.get_student(self.request.POST.get('std_id')).get_absolute_url()

    def check_if_num(self, std_id):
        try:
            std_id = int(std_id)

            return std_id
        except:
            raise Http404

    def get_student(self, std_id):
        pk = self.check_if_num(std_id)
        student = get_object_or_404(Student, pk=pk)
        return student

    def form_valid(self, form):
        student = self.get_student(self.request.POST.get('std_id'))
        self.object = form.save(commit=False)
        self.object.student = student
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['student'] = self.get_student(self.request.GET.get('std_id'))
        
        return context


class EditResultsPaperView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    context_object_name = 'results_paper'
    queryset = ResultsPaper.objects.all()
    form_class = AddResultsPaperForm
    template_name = 'students/add_results_paper.html'
    success_message = _('The result paper has been modified')


class DeleteResultsPaperView(LoginRequiredMixin,DeleteSuccessMessageMixin,DeleteView):
    queryset = ResultsPaper.objects.all()
    form_class = AddResultsPaperForm
    template_name = 'students/delete_results_papaer_confirm.html'
    success_message = _('The result paper has been deleted')

    def get_success_url(self, *args, **kwargs):
        return self.object.student.get_absolute_url()

@login_required
def semester_edit_view(request, pk, std_id):
    semester = get_object_or_404(Semester, pk=pk)

    if str(semester.order) == '3':
        form = AddSubjectResultSemester3Form
    else:
        form = AddSubjectResultForm
    
    formset = subjects_results_formset(form)(request.POST or None, queryset=SubjectResult.objects.filter(semester__id=pk))
    if request.method == 'POST':
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.save()
            semester_order = SEMESTERS_DIC.get(str(semester.order))
            if get_language() == 'ar':
                msg = 'تم تعديل بيانات الفترة {}'.format(semester_order)
            else:
                msg = '{} semester info has been modified'.format(semester_order)
            messages.success(request,msg.capitalize())
            return redirect('students:detail', pk=std_id)

    context = {'formset': formset, 'semester': semester}
    return render(request, 'students/semester_edit.html', context)


@login_required
def edit_class_grades_view(request, pk, order=1):
    the_class = TheClass.objects.get(pk=pk)
    if not str(order) in ['1', '2', '3']:
        order = '1'
    qs = ClassGrade.objects.filter(the_class=the_class, order=order)
    if str(order) != '3':
        form = AddClassGradesForm
    else :
        form = AddClassGradesSemester3Form
    formset = edit_class_grades_formset(form)(request.POST or None, queryset=qs)
    order = str(order)
    
    if request.method == 'POST':
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.save()
            msg = 'The {} Semester grades for {} Class have been modified'.format(SEMESTERS_DIC.get(order),
                                                                the_class.name) 
            if get_language() == 'ar':
                msg = 'تم تعديل درجات الفترة {} للصف {}'.format(SEMESTERS_DIC.get(order),
                                                                the_class.name)            
            messages.success(request,msg)            
            return redirect('main:classes-dashboard')
    context = {'formset': formset,

               'order': SEMESTERS_DIC.get(order),
               'class_name': the_class.name}
    return render(request, 'students/edit_class_grades.html', context)

@login_required
def add_compensatory_view(request, pk, part):
    qs = CompensatoryExam.objects.filter(results_paper__id=pk, part=part)
    formset = com_exams_formset(request.POST or None, queryset=qs)
    paper = get_object_or_404(ResultsPaper, id=pk)
    if request.method == 'POST':
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    if form.instance.id:
                        form.instance.delete()
                else:
                    if form.is_valid():
                        if form.instance.subject:
                            obj = form.save(commit=False)
                            obj.results_paper = paper
                            obj.save()
            attempt = HUMAN_COUNTER_DIC.get(str(part))
            if get_language() == 'ar':
                msg = 'تم تعديل نتائج الدور {}'.format(attempt)
            else:
                msg = 'The {} attempt results have been modified '.format(attempt)
            messages.success(request,msg)
            return redirect(paper.student.get_absolute_url())
    context = {'formset': formset, 'paper': paper,
               'part': PART_DIC.get(str(part))}
    return render(request, 'students/add_compensatory_exam_result.html', context)

@login_required
def semester_activation_toggle_view(request, pk):
    semester, toggle = Semester.objects.toggle(pk)
    if request.is_ajax():
        json_data = {'active': toggle}
        return JsonResponse(json_data)
    return redirect(semester.get_absolute_url())

@login_required
def compensatory_toggle_view(request, paper_id, part):
    toggle = {True:_('Hide'),False:_('Show')}
    target = None
    paper = get_object_or_404(ResultsPaper,id=paper_id)
    if part == 2:
        paper.part2 = not paper.part2
        target = paper.part2
    elif part == 3:
        paper.part3 = not paper.part3
        target = paper.part3
    else:
        return Http404
    paper.save()
    if request.is_ajax():
        json_data = {'toggle': toggle.get(target)}
        return JsonResponse(json_data)
    return redirect(paper.get_absolute_url())

@login_required
def results_activation_confirm_view(request, status, pk):
    classroom = get_object_or_404(ClassRoom, pk=pk)
    text = _('Activate')
    if not bool(status):
        text = _('Deactivate')
    if request.method == 'POST':
        results = ResultsPaper.objects.filter(student__classroom=classroom)
        results.update(active=bool(status))        
        if get_language() == 'ar':
            msg = 'تم {} جميع نتائج الفصل {}'.format(text,classroom.name)
        else :
            msg = 'All {} results has been {}d'.format(classroom.name,text).capitalize()
        messages.success(request,msg)
        return redirect('main:students-classrooms-dashboard')
    context = {
        'classroom_name': classroom.name,
        'status': text}
    return render(request, 'students/results_activation_confirm.html', context)

@login_required
def results_activation_toggle_view(request, pk, status):
    status = bool(status)
    classroom = get_object_or_404(ClassRoom, pk=pk)
    results = ResultsPaper.object.filter(student__classroom=classroom)
    return redirect('main:users-dashboard')
