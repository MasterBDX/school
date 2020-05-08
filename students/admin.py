from django.contrib import admin

from students.models import (Student, ResultsPaper, ClassGrade,
                             Semester, SubjectResult, CompensatoryExam)

admin.site.register(Student)
admin.site.register(ResultsPaper)
admin.site.register(Semester)
admin.site.register(SubjectResult)
admin.site.register(ClassGrade)
admin.site.register(CompensatoryExam)
