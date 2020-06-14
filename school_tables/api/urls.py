from django.urls import path

from .views import ScheduleApiView, ExamsTabelApiView


app_name = 'school_tables'
urlpatterns = [
    path('classroom-schedule/<int:pk>', ScheduleApiView.as_view(),
         name='classroom-schedule'),
    path('exams-table/', ExamsTabelApiView.as_view(),
         name='exams-table')
]
