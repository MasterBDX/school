from .models import SchoolInfo


def school_name(request):
    qs = SchoolInfo.objects.all()
    if qs.exists():
        obj = qs.first()
        return {'school_name': obj.name}
    return None
