from django.urls import path
from django.conf import settings

from .views import (StudentDetail, StudentPrintableDetail,
                    AddStudentView, EditStudentView,
                    DeleteStudentView, SearchStudentsView,
                    AddResultsPaperView, EditResultsPaperView,
                    DeleteResultsPaperView, semester_edit_view,
                    edit_class_grades_view, add_compensatory_view,
                    semester_active_toggle_view, results_activation_confirm_view)

app_name = 'students'
urlpatterns = [
    path('<int:pk>-detail/', StudentDetail.as_view(), name='detail'),
    path('<int:pk>-printable-detail/', StudentPrintableDetail.as_view(),
         name='printable-detail'),
    path('add/', AddStudentView.as_view(),
         name='add'),
    path('edit/<int:pk>/', EditStudentView.as_view(),
         name='edit'),

    path('delete/<int:pk>/', DeleteStudentView.as_view(),
         name='delete'),

    path('search/', SearchStudentsView.as_view(),
         name='search'),

    path('add-results-paper/', AddResultsPaperView.as_view(),
         name='add-results-paper'),
    path('<int:pk>/edit-results-paper/', EditResultsPaperView.as_view(),
         name='edit-results-paper'),

    path('<int:pk>/delete-results-paper/', DeleteResultsPaperView.as_view(),
         name='delete-results-paper'),

    path('<int:std_id>/semesters/<int:pk>/edit/', semester_edit_view,
         name='semester-edit'),

    path('<int:pk>/edit-class-grades/order-<int:order>/', edit_class_grades_view,
         name='edit-class-grades'),


    path('compensatory-exam/add/<int:pk>/part-<int:part>/',
         add_compensatory_view, name='compensatory-exam-add'),
    path('semester-active-toggle/<int:pk>/',
         semester_active_toggle_view, name='semester-active-toggle'),
    path('results-activation-confirm/<int:status>/classroom-<int:pk>',
         results_activation_confirm_view, name='results-activation-confirm'),
]
