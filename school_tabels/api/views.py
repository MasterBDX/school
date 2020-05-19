from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from school_tabels.models import ClassRoom, ExamTabel
from .serialzers import ScheduleSerialzer, ExamsTabelSerializer


class ScheduleApiView(APIView):
    def get(self, request, pk):
        obj = get_object_or_404(ClassRoom, pk=pk)
        qs = obj.days.all()
        if not qs.exists():
            return Response(status=404)
        schedule_obj = ScheduleSerialzer(qs, many=True)
        return Response(schedule_obj.data)


class ExamsTabelApiView(APIView):
    def get(self, request):
        data = request.GET
        qs = ExamTabel.objects.filter(exam_type=data.get('exam_type', '1'),
                                      year=data.get('year', '3000'),
                                      semester=data.get(
            'semester', '33'),
            the_class=data.get(
            'the_class', '3455'),
            class_room=data.get('class_room', '3455'))
        if qs.exists():
            exam_table = qs.first()
            json_data = ExamsTabelSerializer(exam_table)
            return Response(json_data.data)
        else:
            return Response(status=404)
