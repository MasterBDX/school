from django.shortcuts import (render, get_object_or_404, redirect, Http404)
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView
)
from django.http import JsonResponse


from .filters import get_stds_filters
from .models import Student, ResultsPaper
from school_tabels.models import ClassRoom

from .forms import (AddStudent, AddResultsPaperForm,
                    AddCompensatoryExamForm)

from school_tabels.models import TheClass
from .models import (Student, Semester, SubjectResult,
                     ClassGrade, CompensatoryExam)

from .formsets import (subjects_results_formset,
                       edit_class_grades_formset,
                       com_exams_formset, edit_com_exams_formset)


class StudentDetail(DetailView):
    model = Student
    template_name = 'students/detail.html'


class StudentPrintableDetail(DetailView):
    model = Student
    template_name = 'students/printable_detail.html'


class AddStudentView(CreateView):
    form_class = AddStudent
    template_name = "students/add_student.html"
    success_url = reverse_lazy("main:students-classrooms-dashboard")


class EditStudentView(UpdateView):
    context_object_name = 'student'
    queryset = Student.objects.all()
    form_class = AddStudent
    template_name = "students/add_student.html"
    success_url = reverse_lazy("main:students-classrooms-dashboard")


class DeleteStudentView(DeleteView):
    queryset = Student.objects.all()
    template_name = "students/delete_student_confirm.html"
    success_url = reverse_lazy("main:students-classrooms-dashboard")


class SearchStudentsView(ListView):
    context_object_name = 'students'
    template_name = 'students/search_students.html'

    def get_queryset(self, *args, **kwargs):
        q = self.request.GET.get('q')
        qs = Student.objects.filter(get_stds_filters(q))
        return qs


class AddResultsPaperView(CreateView):
    form_class = AddResultsPaperForm
    template_name = 'students/add_results_paper.html'

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
        context['std_id'] = self.request.GET.get('std_id')
        return context


class EditResultsPaperView(UpdateView):
    queryset = ResultsPaper.objects.all()
    form_class = AddResultsPaperForm
    template_name = 'students/add_results_paper.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['std_id'] = self.request.GET.get('std_id')
        return context


class DeleteResultsPaperView(DeleteView):
    queryset = ResultsPaper.objects.all()
    form_class = AddResultsPaperForm
    template_name = 'students/delete_results_papaer_confirm.html'

    def get_success_url(self, *args, **kwargs):
        return self.object.student.get_absolute_url()


def semester_edit_view(request, pk, std_id):
    semester = get_object_or_404(Semester, pk=pk)

    formset = subjects_results_formset(
        request.POST or None, queryset=SubjectResult.objects.filter(semester__id=pk))
    if request.method == 'POST':
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.save()
            return redirect('students:detail', pk=std_id)

    context = {'formset': formset, 'semester': semester}
    return render(request, 'students/semester_edit.html', context)


def get_human_order(order):
    order_dic = {'1': 'الأول', '2': 'الثاني', '3': 'الثالث'}
    return order_dic.get(order, 'الأول')


def edit_class_grades_view(request, pk, order='1'):
    the_class = TheClass.objects.get(pk=pk)
    if not str(order) in ['1', '2', '3']:
        order = '1'
    qs = ClassGrade.objects.filter(the_class=the_class, order=order)

    formset = edit_class_grades_formset(request.POST or None, queryset=qs)
    if request.method == 'POST':
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.save()
            return redirect('main:classes-dashboard')
    context = {'formset': formset,
               'order': get_human_order(order),
               'class_name': the_class.name}
    return render(request, 'students/edit_class_grades.html', context)


PART = {'2': 'الثاني',
        '3': 'الثالث'}


def add_compensatory_view(request, pk, part):
    qs = CompensatoryExam.objects.filter(results_paper__id=pk, part=part)
    formset = com_exams_formset(request.POST or None, queryset=qs)
    paper = get_object_or_404(ResultsPaper, id=pk)
    if request.method == 'POST':
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    if form.instance.subject:
                        obj = form.save(commit=False)
                        obj.results_paper = paper
                        obj.save()
            return redirect('/')
    context = {'formset': formset, 'paper': paper, 'part': PART.get(str(part))}
    return render(request, 'students/add_compensatory_exam.html', context)


def semester_active_toggle_view(request, pk):
    semester, toggle = Semester.objects.toggle(pk)
    if request.is_ajax():
        json_data = {'active': toggle}
        return JsonResponse(json_data)
    return redirect(semester.get_absolute_url())


def results_activation_confirm_view(request, status, pk):
    classroom = get_object_or_404(ClassRoom, pk=pk)
    text = 'تنشيط'
    if not bool(status):
        text = 'إلغاء تنشيط'
    if request.method == 'POST':
        results = ResultsPaper.objects.filter(student__classroom=classroom)
        results.update(active=bool(status))

        return redirect('main:students-classrooms-dashboard')
    context = {
        'classroom_name': classroom.name,
        'status': text}
    return render(request, 'students/results_activation_confirm.html', context)


def results_activation_toggle_view(request, pk, status):
    status = bool(status)
    classroom = get_object_or_404(ClassRoom, pk=pk)
    results = ResultsPaper.object.filter(student__classroom=classroom)
    return redirect('main:users-dashboard')
