from django.urls import path, re_path
from django.conf import settings

from .views import (HomeView, AboutusView, ClassesScheduleDashboardView,
                    contact_view, ExamsDashboardView,
                    ClassesDashboardView, ClassroomsDashboardView,
                    StudentsDashboardView, StudentsClassroomsDashboardView,
                    PostsDashboardView, SubjectsDashboardView,
                    StudentsDistributionView, StdsClassroomDistributionView,
                    ResultSearchView, get_result_view, UsersDashboard,
                    SchoolInfoEditView, main_articles_edit_view, lang_change_view)


app_name = 'main'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about-us/', AboutusView.as_view(), name='about_us'),
    path('contact-us/', contact_view, name='contact'),
    path('exams-dashboard/',
         ExamsDashboardView.as_view(), name='exams-dashboard'),
    path('classes-tabel-dashboard', ClassesScheduleDashboardView.as_view(),
         name='classes-tabel-dashboard'),
    path('students-classrooms-dashboard/', StudentsClassroomsDashboardView.as_view(),
         name='students-classrooms-dashboard'),
    path('students-dashboard/<int:pk>/', StudentsDashboardView.as_view(),
         name='students-dashboard'),
    path('students-distribution/', StudentsDistributionView.as_view(),
         name='students-distribution'),
    path('students-search/', StdsClassroomDistributionView.as_view(),
         name='students-search'),
    path('students-classroom-distribution/<int:pk>/', StdsClassroomDistributionView.as_view(),
         name='students-classroom-distribution'),
    path('classes-dashboard/', ClassesDashboardView.as_view(),
         name='classes-dashboard'),
    path('classrooms-dashboard/', ClassroomsDashboardView.as_view(),
         name='classrooms-dashboard'),
    path('subjects-dashboard/', SubjectsDashboardView.as_view(),
         name='subjects-dashboard'),
    path('posts-dashboard', PostsDashboardView.as_view(), name='posts-dashboard'),
    path('users-dashboard', UsersDashboard.as_view(), name='users-dashboard'),
    path('result-search', ResultSearchView.as_view(), name='result-search'),
    path('result-doc', get_result_view, name='result-doc'),
    path('school-info/edit/', SchoolInfoEditView.as_view(), name='school-info-edit'),
    path('main-articles/edit/', main_articles_edit_view,
         name='main-articles-edit'),
    re_path(r'^lang-change/(?P<lang>\w{2})/$', lang_change_view,
            name='lang-change')



]
