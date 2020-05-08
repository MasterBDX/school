from django.contrib import admin

from .models import (TheClass, Day,
                     Article, ClassRoom,
                     SchoolSchedule, Exam,
                     ExamTabel)

admin.site.register(TheClass)
admin.site.register(Day)
admin.site.register(Article)
admin.site.register(ClassRoom)
admin.site.register(Exam)
admin.site.register(ExamTabel)
admin.site.register(SchoolSchedule)
