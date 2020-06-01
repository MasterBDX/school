from django.db import models
from django.utils.translation import ugettext_lazy as _

class StudentManager(models.Manager):
    def same_class(self, id):
        return self.get_queryset().filter(the_class__id=id)


class SemesterManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(active=True)

    def toggle(self, pk):
        active = 'يوجد خطأ'
        qs = self.get_queryset().filter(id=pk)
        if qs.count() == 1:
            obj = qs.first()
            if obj.active:
                obj.active = False
                obj.save()
                active = _('Show')
            else:
                obj.active = True
                obj.save()
                active = _('Hide')
        return obj, active
