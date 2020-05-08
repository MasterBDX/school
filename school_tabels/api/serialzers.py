from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from school_tabels.models import SchoolSchedule, ExamTabel, Exam

from ..vars import TYPE_DIC, SEMESTERS_DIC


class ScheduleSerialzer(serializers.ModelSerializer):
    class_1 = SerializerMethodField()
    class_2 = SerializerMethodField()
    class_3 = SerializerMethodField()
    class_4 = SerializerMethodField()
    class_5 = SerializerMethodField()
    class_6 = SerializerMethodField()
    class_7 = SerializerMethodField()
    day = SerializerMethodField()
    class_room = SerializerMethodField()

    class Meta:
        model = SchoolSchedule
        fields = '__all__'

    def get_class_1(self, obj):
        return obj.class_1.name

    def get_class_2(self, obj):
        return obj.class_2.name

    def get_class_3(self, obj):
        return obj.class_3.name

    def get_class_4(self, obj):
        return obj.class_4.name

    def get_class_5(self, obj):
        return obj.class_5.name

    def get_class_6(self, obj):
        return obj.class_6.name

    def get_class_7(self, obj):
        return obj.class_7.name

    def get_day(self, obj):
        return obj.day.name

    def get_class_room(self, obj):
        return obj.class_room.name


class ExamSerializer(serializers.ModelSerializer):
    start_time = SerializerMethodField()
    end_time = SerializerMethodField()

    class Meta:
        model = Exam
        exclude = ['exam_tabel', 'timestamp', 'updated']

    def get_start_time(self, obj):
        return obj.start_time.strftime('%H:%M')

    def get_end_time(self, obj):
        return obj.end_time.strftime('%H:%M')


class ExamsTabelSerializer(serializers.ModelSerializer):
    exam = SerializerMethodField()
    exam_type = SerializerMethodField()
    the_class = SerializerMethodField()
    class_room = SerializerMethodField()
    semester = SerializerMethodField()

    class Meta:
        model = ExamTabel
        exclude = ['last_update_by', 'timestamp', 'updated']

    def get_exam(self, obj):
        return ExamSerializer(obj.exams.all(), many=True).data

    def get_exam_type(self, obj):
        return TYPE_DIC.get(obj.exam_type)

    def get_the_class(self, obj):
        return obj.the_class.name

    def get_class_room(self, obj):
        return obj.class_room.name

    def get_semester(self, obj):
        return SEMESTERS_DIC.get(obj.semester)
