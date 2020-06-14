from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (TemplateView, ListView,
                                  FormView, DetailView,
                                  UpdateView)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.utils import translation
from django.utils.translation import ugettext as _
from django.utils.http import is_safe_url



from .forms import (Contact, ResultSearchForm, MainArticleForm,
                    SchoolInfoForm, MainArticleForm)
from posts.models import Post
from school_tables.models import (Article, Exam, TheClass, ClassRoom)
from students.models import Student, ResultsPaper,Semester
from students.filters import get_stds_filters
from .models import SchoolInfo, MainArticle
from .mixins import AdminPermission

class HomeView(TemplateView):
    template_name = 'main/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_artcles = MainArticle.objects.all()[:3]
        context['main_articles'] = main_artcles
        context['last_posts'] = Post.objects.active()[:3]
        return context


class AboutusView(TemplateView):
    template_name = 'main/about_us.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = SchoolInfo.objects.all().first()
        return context


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

            txt_ = get_template(
                'main/snippets/message.txt').render(msg_context)
            html_ = get_template(
                'main/snippets/html_message.html').render(msg_context)

            send_mail(
                name,
                txt_,
                from_email,
                [settings.MAIN_EMAIL],
                html_message=html_,
                fail_silently=False
            )

            messages.add_message(request, messages.SUCCESS,
                                 _('Thank you for contacting us'))
            return redirect('main:contact')
    context = {'form': form}
    return render(request, 'main/contact.html', context)


class ExamsDashboardView(LoginRequiredMixin, ListView):
    context_object_name = 'exams'
    queryset = Exam.objects.all()
    template_name = 'main/exams_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = TheClass.objects.all()
        return context


class ClassesScheduleDashboardView(LoginRequiredMixin, ListView):
    context_object_name = 'class_rooms'
    queryset = ClassRoom.objects.all()
    template_name = 'main/classes_schedule_dashboard.html'


class ClassesDashboardView(LoginRequiredMixin,ListView):
    context_object_name = 'classes'
    queryset = TheClass.objects.all()
    template_name = 'main/classes_dashboard.html'


class ClassroomsDashboardView(LoginRequiredMixin,ListView):
    context_object_name = 'classrooms'
    queryset = ClassRoom.objects.select_related('the_class')
    template_name = 'main/classrooms_dashboard.html'


class SubjectsDashboardView(LoginRequiredMixin, ListView):
    context_object_name = 'subjects'
    queryset = Article.objects.all()
    template_name = 'main/subjects-dashboard.html'


class PostsDashboardView(LoginRequiredMixin, ListView):
    context_object_name = 'posts'
    queryset = Post.objects.all()
    template_name = 'main/posts-dashboard.html'


class StudentsClassroomsDashboardView(LoginRequiredMixin,ListView):
    context_object_name = 'classes'
    queryset = TheClass.objects.all()
    template_name = 'main/students_classroom_dashboard.html'


class StudentsDashboardView(LoginRequiredMixin,ListView):
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
            result = _('Not Exist')
            if student.get('id') in self.obj.get_results():
                result = _('Exist')
            student.update({'result': result,
                            'full_name': self.get_full_name(student)})
        return context


class StudentsListView(ListView):
    template_name = 'main/students_classroom_list.html'
    context_object_name = 'classes'
    queryset = TheClass.objects.all()


class StdsClassroomListView(ListView):
    template_name = 'main/students_list.html'
    context_object_name = 'students'

    def get_queryset(self, *args, **kwargs):
        self.obj = get_object_or_404(
            ClassRoom, pk=self.kwargs.get('pk', '1'))
        return self.obj.students.same_class(self.obj.the_class.id)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.obj:
            context['classroom_name'] = self.obj.name

        return context

def get_result_view(request):
    form = ResultSearchForm(request.GET or None)
    if form.is_valid():
        the_class = form.cleaned_data.get('the_class')
        std_id = form.cleaned_data.get('id_num')
        obj = ResultsPaper.objects.select_related('student','the_class') \
            .filter(the_class=the_class).filter(
            Q(student__id=std_id) | Q(student__nid_number=std_id)).first()
        if obj:
            semesters = Semester.objects.active().filter(results_paper=obj)
            context = {'object': obj,'semesters':semesters,'std_name':obj.student.get_std_name()}
            return render(request, 'main/result_doc.html', context)
        else:
            msg = _(
                'You entered the data incorrectly Please check your information')
            messages.add_message(request, messages.WARNING, msg)
    return redirect('main:result-search')


class ResultSearchView(FormView):
    form_class = ResultSearchForm
    template_name = 'main/result_search.html'


User = get_user_model()

class UsersDashboard(LoginRequiredMixin,AdminPermission,ListView):
    queryset = User.objects.all_users()
    template_name = 'main/users_dashboard.html'
    context_object_name = 'users'


class SchoolInfoEditView(LoginRequiredMixin,AdminPermission,UpdateView):
    queryset = SchoolInfo.objects.all()
    form_class = SchoolInfoForm
    template_name = 'main/school_info_edit.html'
    success_url = reverse_lazy('main:about_us')

    def get_object(self, queryset=None):
        qs = SchoolInfo.objects.all()
        if qs.exists():
            obj = qs.first()

            return obj
        raise Http404


class MainArticlesDashboard(LoginRequiredMixin,AdminPermission,ListView):
    context_object_name = 'quotes'
    queryset = MainArticle.objects.all()[:8]
    template_name = 'main/main_articles_dashboard.html'


class MainArticlesEditView(LoginRequiredMixin,AdminPermission,UpdateView):
    queryset = MainArticle.objects.all()
    form_class = MainArticleForm
    template_name = 'main/main_articles_edit.html'
    success_url = reverse_lazy('main:main-articles-dashboard')
    


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
