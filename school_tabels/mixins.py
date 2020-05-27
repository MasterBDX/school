from django.contrib import messages

class DeleteSuccessMessageMixin:
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
