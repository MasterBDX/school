from django.urls import path, include

from .views import (AddClassView, EditClassView,
                    DeleteClassView,
                    add_edit_exam_table_view,
                    DeleteExamTableView,
                    add_edit_full_schedule_view,
                    delete_full_schedule_view,
                    AddClassRoomView, EditClassRoomView,
                    DeleteClassroomView, AddSubjectView,
                    EditSubjectView, DeleteSubjectView,
                    ScheduleDetailView, ExamstableDetailView)


app_name = 'school_tables'
urlpatterns = [
    path('subjects/add/', AddSubjectView.as_view(), name='subjects-add'),
    path('subjects/<int:pk>/edit', EditSubjectView.as_view(), name='subjects-edit'),
    path('subjects/<int:pk>/delete',
         DeleteSubjectView.as_view(), name='subjects-delete'),
    path('classes/add/', AddClassView.as_view(), name='add_class'),
    path('classes/<int:pk>/edit/', EditClassView.as_view(), name='edit_class'),
    path('class/<int:pk>/delete/', DeleteClassView.as_view(), name='delete_class'),
    path('classrooms/add/', AddClassRoomView.as_view(), name='classrooms-add'),
    path('classroom/<int:pk>/edit/',
         EditClassRoomView.as_view(), name='classrooms-edit'),
    path('classroom/<int:pk>/delete/',
         DeleteClassroomView.as_view(), name='classrooms-delete'),
    path('exams-table/add/', add_edit_exam_table_view, name='exams-tables-add'),
    path('exams-table/<int:pk>/edit/', add_edit_exam_table_view,
         name='exams-tables-edit'),
    path('exams-table/<int:pk>/delete/', DeleteExamTableView.as_view(),
         name='exams-tables-delete'),
    path('full-schedule/add/', add_edit_full_schedule_view,
         name='add-full-schedule'),
    path('full-schedule/edit/<int:class_id>/', add_edit_full_schedule_view,
         name='edit-full-schedule'),

    path('full-schedule/<int:class_id>/delete/', delete_full_schedule_view,
         name='delete-full-schedule'),
    path('schedule-detail/', ScheduleDetailView.as_view(),
         name='schedule-detail'),
    path('exams-table-detail/', ExamstableDetailView.as_view(),
         name='exams-table-detail'),


    path('api/', include('school_tables.api.urls', namespace='api'))


]
