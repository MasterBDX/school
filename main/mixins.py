from django.contrib import messages
from django.urls import reverse_lazy

class DeleteSuccessMessageMixin:
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class StudentSuccessUrlMixin:
    def get_success_url(self):
        classroom_id = self.object.classroom.id
        success_url = reverse_lazy("main:students-dashboard",
                                    kwargs={'pk':classroom_id})
        return success_url