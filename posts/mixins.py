from django.http import Http404


class OwnUserObjectMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=None)
        user = self.request.user
        if obj.author == user:
            return obj
        raise Http404


class OUOAndAdminMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=None)
        user = self.request.user
        if obj.author == user or user.is_admin:
            return obj
        raise Http404
