from .models import SchoolInfo


def school_name(request):
    qs = SchoolInfo.objects.all()
    if qs.exists():
        obj = qs.first()
        return {'school_ar_name': obj.name,
                'school_en_name': obj.english_name}
    return {}
