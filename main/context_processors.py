from .models import SchoolInfo


def school_name(request):
    obj = SchoolInfo.objects.all().first()
    if obj:
        return {'school_name':obj.get_name()}
    return {}
