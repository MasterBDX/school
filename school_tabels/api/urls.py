from django.urls import path

from .views import ScheduleApiView, ExamsTabelApiView


app_name = 'school_tabels'
urlpatterns = [
    path('classroom-schedule/<int:pk>', ScheduleApiView.as_view(),
         name='classroom-schedule'),
    path('exams-tabel/', ExamsTabelApiView.as_view(),
         name='exams-tabel')
]
