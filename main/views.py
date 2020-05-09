from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (TemplateView, ListView,
                                  FormView, DetailView,
                                  UpdateView)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.utils import translation
from django.utils.http import is_safe_url

from .formsets import MainArticleFormset
from .forms import (Contact, ResultSearchForm, MainArticleForm,
                    SchoolInfoForm, MainArticleForm)

from posts.models import Post

from school_tabels.models import (Article, Exam, TheClass, ClassRoom)

from students.models import Student, ResultsPaper
from students.filters import get_stds_filters

from .models import SchoolInfo, MainArticle


class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        main_artcles = MainArticle.objects.all()
        if main_artcles.count() >= 3:
            main_artcles = main_artcles[:3]

        context['main_articles'] = main_artcles
        context['last_posts'] = Post.objects.all()[:3]
        return context


class AboutusView(TemplateView):
    template_name = 'main/about_us.html'


def contact_view(request):
    form = Contact()
    if request.method == 'POST':
        form = Contact(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            from_email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            phone_num = form.cleaned_data.get('phone_number')
            message = form.cleaned_data.get('message')
            msg_context = {'name': name, 'subject': subject,
                           'message': message, 'phone': phone_num}
            print(msg_context)
            txt_ = get_template(
                'main/snippets/message.txt').render(msg_context)
            html_ = get_template(
                'main/snippets/html_message.html').render(msg_context)

            send_mail(
                name,
                txt_,
                from_email,
                ['masterbdxteam@gmail.com'],
                html_message=html_,
                fail_silently=False
            )

            messages.add_message(request, messages.SUCCESS,
                                 'your message has been sent')
            return redirect('/#contact')
    context = {'form': form}
    return render(request, 'main/contact.html', context)


class ExamsDashboardView(ListView):
    context_object_name = 'exams'
    queryset = Exam.objects.all()
    template_name = 'main/exams_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = TheClass.objects.all()
        return context


class ClassesScheduleDashboardView(ListView):
    context_object_name = 'class_rooms'
    queryset = ClassRoom.objects.all()
    template_name = 'main/classes_schedule_dashboard.html'


class ClassesDashboardView(ListView):
    context_object_name = 'classes'
    queryset = TheClass.objects.all()
    template_name = 'main/classes_dashboard.html'


class ClassroomsDashboardView(ListView):
    context_object_name = 'classrooms'
    queryset = ClassRoom.objects.all()
    template_name = 'main/classrooms_dashboard.html'


class SubjectsDashboardView(ListView):
    context_object_name = 'subjects'
    queryset = Article.objects.all()
    template_name = 'main/subjects-dashboard.html'


class PostsDashboardView(ListView):
    context_object_name = 'posts'
    queryset = Post.objects.all()
    template_name = 'main/posts-dashboard.html'


class StudentsClassroomsDashboardView(ListView):
    context_object_name = 'classes'
    queryset = TheClass.objects.all()
    template_name = 'main/students_classroom_dashboard.html'


class StudentsDashboardView(ListView):
    context_object_name = 'students'
    template_name = 'main/students_dashboard.html'

    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        self.obj = get_object_or_404(ClassRoom, pk=pk)
        return self.obj.students.same_class(self.obj.the_class.id).values()

    def get_full_name(self, dic):
        full_name = "{}  {}  {}  {}".format(
            dic.get('first_name', ''), dic.get('father_name', ''),
            dic.get('grand_father_name', ''), dic.get('surname', ''))
        return full_name

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['classroom_name'] = self.obj.name

        for student in context['students']:
            result = 'غير موجودة'
            if student.get('id') in self.obj.get_results():
                result = 'موجودة'
            student.update({'result': result,
                            'full_name': self.get_full_name(student)})
        return context


class StudentsDistributionView(ListView):
    template_name = 'main/students_distribution.html'
    context_object_name = 'classes'
    queryset = TheClass.objects.all()


class StdsClassroomDistributionView(ListView):
    template_name = 'main/students_classroom_distribution.html'
    context_object_name = 'students'

    def get_queryset(self, *args, **kwargs):
        self.obj = ''
        q = self.request.GET.get('q')
        if q != None and q != ' ':
            qs = Student.objects.filter(get_stds_filters(q))
            return qs

        self.obj = get_object_or_404(
            ClassRoom, pk=self.kwargs.get('pk', '1'))
        return self.obj.students.same_class(self.obj.the_class.id)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.obj:
            context['classroom_name'] = self.obj.name
        return context


class ResultSearchView(FormView):
    form_class = ResultSearchForm
    template_name = 'main/result_search.html'


def get_result_view(request):
    form = ResultSearchForm(request.POST)
    result_paper = None
    if request.method == 'POST':
        if form.is_valid():
            the_class = form.cleaned_data.get('the_class')
            std_id = form.cleaned_data.get('id_num')
            qs = ResultsPaper.objects.filter(the_class=the_class).filter(
                Q(student__id=std_id) | Q(student__id_number=std_id))

            if qs.exists():
                result_paper = qs.first()
            else:
                msg = 'لقد قمت بإدخال البيانات بشكل خاطئ يرجى التأكد من البيانات'
                messages.add_message(request, messages.WARNING, msg)
                return redirect('main:result-search')

    context = {'object': result_paper}
    return render(request, 'main/result_doc.html', context)


User = get_user_model()


class UsersDashboard(ListView):
    queryset = User.objects.all_users()
    template_name = 'main/users_dashboard.html'
    context_object_name = 'users'


class SchoolInfoEditView(UpdateView):
    queryset = SchoolInfo.objects.all()
    form_class = SchoolInfoForm
    template_name = 'main/school_info_edit.html'
    success_url = reverse_lazy('main:school-info-edit')

    def get_object(self, queryset=None):
        qs = SchoolInfo.objects.all()
        if qs.exists():
            obj = qs.first()

            return obj
        raise Http404


def main_articles_edit_view(request):
    qs = MainArticle.objects.all()
    formset = MainArticleFormset(request.POST or None, queryset=qs)
    if request.method == 'POST':
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.save()
            return redirect(request.path)
    context = {'formset': formset}
    return render(request, 'main/main_articles_edit.html', context)


def lang_change_view(request, lang):
    next_ = request.GET.get('next')
    if lang in ['ar', 'en']:
        request.session['lang'] = lang
        translation.activate(lang)
        is_safe = is_safe_url(url=next_,
                              allowed_hosts=settings.ALLOWED_HOSTS,
                              require_https=request.is_secure())
        if not is_safe:
            next_ = reverse('main:home')
        return redirect(next_)

    raise Http404
